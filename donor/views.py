from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import MyWalletSerializer, DonorCardSerializer
from .models import DonorCard
# Create your views here.


class MyWallet(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MyWalletSerializer

    def get_queryset(self):
        return DonorCard.objects.filter(user=self.request.user).order_by('-donorDate')


class DonorCardView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DonorCardSerializer
    lookup_field = 'cardId'
    queryset = DonorCard.objects.all()
