"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import user.views as user_views
import donor.views as donor_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', user_views.UserLogin.as_view()),
    path('register', user_views.UserRegister.as_view()),
    path('getDonorCard', donor_views.MyWallet.as_view()),
    path('getDonorDetail/<str:cardId>', donor_views.DonorCardView.as_view()),
    path('getMyAddress', user_views.WalletAddress.as_view()),
    path('sendDonorCard/<str:cardId>', donor_views.SendDonorCard.as_view()),
    path('getDeliveryList', donor_views.DeliveryList.as_view()),
    path('makeDonorCard/<str:cardId>', donor_views.GenerateDonorCard.as_view()),
]
