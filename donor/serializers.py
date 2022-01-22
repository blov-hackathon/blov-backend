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

    class Meta:
        model = Transfer
        fields = "__all__"
        read_only_fields = ('id',)

    def get_deliveryType(self, obj):
        if self.context['request'].user == obj.fromUser:
            return 'send'
        return 'recieve'
