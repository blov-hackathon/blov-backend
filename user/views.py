from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import User, AuthToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserSerializer
from donor.models import DonorCard
from datetime import datetime
# Create your views here.


class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            user = User.objects.create_user(
                request.data['phone_number'], request.data['name'], request.data['blood_type'], request.data['password'])
            user.save()
            # generate random 6 digit number
            DonorCard.objects.create(user=user, donorDate=datetime.now(), donorType="전혈", donorVolume=320, donorName=user.name,
                                     donorBirth=datetime(2000, 1, 1), donorPlace="인천인하혈액원", cardId=f"1000{str(datetime.now().timestamp()).split('.')[1]}")
            token = AuthToken.objects.create(user=user)
            return Response({'status': 'success', 'message': 'User created successfully', 'token': token.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        phone_number = data.get('phone_number').strip().replace(
            ' ', '').replace('-', '')
        user = authenticate(phone_number=phone_number,
                            password=data.get('password'))
        if user is not None:
            token = AuthToken.objects.create(user=user)
            return Response({'status': 'success', 'token': token.id})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'status': 'fail'})


class WalletAddress(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            return Response({'status': 'success', 'address': request.user.address})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
