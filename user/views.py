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
# Create your views here.


class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.create_user(
                request.data['phone_number'], request.data['name'], request.data['blood_type'], request.data['password'])
            user.save()
            token = AuthToken.objects.create(user=user)
            return Response({'status': 'success', 'message': 'User created successfully', 'token': token.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
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
