from django.shortcuts import render, HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import MyWalletSerializer, DonorCardSerializer, TransferSerializer
from .models import DonorCard, Transfer
from user.models import User
from config.ethereum import w3
from django.conf import settings
from donor.ImageGenerator.generator import DonorCardGenerator
from django.core.files import File
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


class SendDonorCard(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            donorCard = DonorCard.objects.get(cardId=kwargs['cardId'])
            fromUser = request.user
            toUser = User.objects.get(address=request.data['targetId'])
            assert donorCard.user == fromUser
            donorCard.user = toUser
            contract = w3.eth.contract(
                settings.ETH_CONTRACT_ADDRESS, abi=settings.ETH_CONTRACT_ABI)
            nonce = w3.eth.get_transaction_count(settings.ETH_WALLET_ADDRESS)
            gas = contract.functions.adminTransferFrom(
                fromUser.address, toUser.address, int(donorCard.cardId)).estimateGas({
                    'from': settings.ETH_WALLET_ADDRESS,
                })
            gasprice = int(w3.eth.generateGasPrice() * 2)
            print(settings.ETH_WALLET_ADDRESS, nonce, gas, gasprice)
            txn = contract.functions.adminTransferFrom(
                fromUser.address, toUser.address, int(donorCard.cardId)).buildTransaction({
                    'from': settings.ETH_WALLET_ADDRESS,
                    'chainId': 4,
                    'gasPrice': gasprice,
                    'gas': gas,
                    'nonce': nonce,
                })
            signed_txn = w3.eth.account.sign_transaction(
                txn, private_key=settings.ETH_WALLET_PRIVATE_KEY)
            w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            Transfer.objects.create(
                fromUser=fromUser, toUser=toUser, donorCard=donorCard, txid=signed_txn.hash.hex())
            donorCard.save()
            return Response({'status': 'success', 'message': 'DonorCard created successfully', 'txid': signed_txn.hash.hex()}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TransferSerializer

    def get_queryset(self):
        return (Transfer.objects.filter(fromUser=self.request.user) | Transfer.objects.filter(toUser=self.request.user)).order_by('-deliveryDate')


class GenerateDonorCard(APIView):

    def get(self, request, cardId):

        input_id = request.GET['inputImageId']
        input_text = request.GET['inputText']

        card = DonorCard.objects.get(cardId=cardId)
        generator = DonorCardGenerator()

        generator.write_user_image(input_id)
        generator.write_template_text(card.donorDate.strftime("%Y.%m.%d"),
                                      card.donorPlace,
                                      card.donorType,
                                      str(card.donorVolume),
                                      card.cardId)
        generator.write_user_text(input_text)

        data = File(generator.get_binary_image())

        return HttpResponse(data, content_type='image/png')

    def post(self, request, cardId):

        input_id = request.data['inputImageId']
        input_text = request.data['inputText']

        card = DonorCard.objects.get(cardId=cardId)
        generator = DonorCardGenerator()

        generator.write_user_image(input_id)
        generator.write_template_text(card.donorDate.strftime("%Y.%m.%d"),
                                      card.donorPlace,
                                      card.donorType,
                                      str(card.donorVolume),
                                      card.cardId)
        generator.write_user_text(input_text)

        card.cardImage.save("{}.png".format(card.id), File(
            generator.get_binary_image()), save=True)

        contract = w3.eth.contract(
            settings.ETH_CONTRACT_ADDRESS, abi=settings.ETH_CONTRACT_ABI)
        nonce = w3.eth.get_transaction_count(settings.ETH_WALLET_ADDRESS)
        gas = contract.functions.mint(
            card.user.address, int(card.cardId), card.cardImage.url).estimateGas({
                'from': settings.ETH_WALLET_ADDRESS,
            })
        gasprice = int(w3.eth.generateGasPrice() * 2)
        txn = contract.functions.mint(
            card.user.address, int(card.cardId), card.cardImage.url).buildTransaction({
                'from': settings.ETH_WALLET_ADDRESS,
                'chainId': 4,
                'gasPrice': gasprice,
                'gas': gas,
                'nonce': nonce,
            })
        signed_txn = w3.eth.account.sign_transaction(
            txn, private_key=settings.ETH_WALLET_PRIVATE_KEY)
        w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        card = DonorCard.objects.get(cardId=cardId)

        return Response({'status': 'success', 'cardImage': card.cardImage.url})
