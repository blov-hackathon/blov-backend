from rest_framework import serializers
from donor.models import DonorCard


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
