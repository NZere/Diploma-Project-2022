from django.shortcuts import render
from django.contrib.auth.models import User, auth
from main.models import ShopToUser
from users.views import get_user_email, get_user_first_name, get_user_last_name
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s: s[0:-ord(s[-1:])]


def index(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
        print(user_first_name)
        if ShopToUser.objects.filter(user=request.user.id).exists():
            return render(request, 'mainApp/homePage_shop.html', {"user_first_name": user_first_name})
    return render(request, 'mainApp/homePage.html',
                  {"user_first_name": user_first_name})  # utir i to cho to передать dictionary

#
# def index(request):
#     if request.user.is_authenticated:
#         if ShopToUser.objects.filter(user=request.user.id).exists():
#             return render(request, 'mainApp/homePage_shop.html')
#     return render(request, 'mainApp/homePage.html')  # utir i to cho to передать dictionary
