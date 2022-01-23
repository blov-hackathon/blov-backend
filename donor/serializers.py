from rest_framework import serializers
from donor.models import DonorCard, Transfer


class MyWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorCard
        fields = ('id', 'cardImage', 'cardId')
        read_only_fields = ('id',)


class DonorCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorCard
        fields = ('id', 'cardImage', 'cardId', 'donorDate', 'donorType',
                  'donorVolume', 'donorName', 'donorBirth', 'donorPlace')
        read_only_fields = ('id',)


class TransferSerializer(serializers.ModelSerializer):
    deliveryType = serializers.SerializerMethodField()
    fromUser = serializers.SerializerMethodField()
    toUser = serializers.SerializerMethodField()
    donorCard = DonorCardSerializer(read_only=True)

    class Meta:
        model = Transfer
        fields = "__all__"
        read_only_fields = ('id',)

    def get_deliveryType(self, obj):
        if self.context['request'].user == obj.fromUser:
            return 'send'
        return 'recieve'

    def get_fromUser(self, obj):
        return obj.fromUser.name

    def get_toUser(self, obj):
        return obj.toUser.name
