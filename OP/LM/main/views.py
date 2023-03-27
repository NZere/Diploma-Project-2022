from datetime import datetime

from django.db import transaction
from rest_framework import generics
from .serializers import *
from django.contrib.auth.decorators import login_required
from .models import Clothes, CartP, CartItemP
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.urls import reverse
from django.utils import timezone
from .models import Clothes, CartP, CartItemP, Block, Coupon, Shops, ShopToUser, CommentaryShops, Purse
from .forms import CouponForm
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib.parse import urlparse

import requests
from django.shortcuts import render, redirect
import hashlib
import json
from time import time
from uuid import uuid4
from django.contrib import messages
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from users.views import encrypt, get_user_email, get_user_first_name, get_user_last_name, get_user_money


def index(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    return render(request, 'clothesL/catalogue.html',
                  {"user_first_name": user_first_name})  # utir i to cho to передать dictionary


def men(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    listMen = Clothes.objects.order_by("-date")
    return render(request, 'clothesL/men.html',
                  {'listMen': listMen, "user_first_name": user_first_name})  # utir i to cho to передать dictionary


def women(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    listW = Clothes.objects.order_by("-date")

    return render(request, 'clothesL/women.html',
                  {'listW': listW, "user_first_name": user_first_name})  # utir i to cho to передать dictionary


def prom(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    listW = Clothes.objects.order_by("-date")
    return render(request, 'clothesL/prom.html',
                  {'listW': listW, "user_first_name": user_first_name})  # utir i to cho to передать dictionary


def newCol(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    listW = Clothes.objects.order_by("-date")
    return render(request, 'clothesL/newCol.html',
                  {'listW': listW, "user_first_name": user_first_name})  # utir i to cho to передать dictionary


def blog(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    return render(request, 'clothesL/blog.html',
                  {"user_first_name": user_first_name})  # utir i to c ho to передать dictionary


def winter(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    return render(request, 'clothesL/winter.html',
                  {"user_first_name": user_first_name})  # utir i to c ho to передать dictionary


def school(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    return render(request, 'clothesL/school.html',
                  {"user_first_name": user_first_name})  # utir i to c ho to передать dictionary


def oscar(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    return render(request, 'clothesL/oscar.html',
                  {"user_first_name": user_first_name})  # utir i to c ho to передать dictionary


def dress(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    return render(request, 'clothesL/dress.html',
                  {"user_first_name": user_first_name})  # utir i to c ho to передать dictionary


def summerCol(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)

    listSummer = []
    listSummer.append(Clothes.objects.get(id=11))

    listSummer.append(Clothes.objects.get(id=12))
    listSummer.append(Clothes.objects.get(id=13))
    listSummer.append(Clothes.objects.get(id=14))
    listSummer.append(Clothes.objects.get(id=15))

    return render(request, 'blog/summer.html', {'listSummer': listSummer,
                                                "user_first_name": user_first_name})  # utir i to c ho to передать dictionary


def winterCol(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    listSummer = []
    listSummer.append(Clothes.objects.get(id=4))

    listSummer.append(Clothes.objects.get(id=5))
    listSummer.append(Clothes.objects.get(id=9))
    return render(request, 'blog/summer.html', {'listSummer': listSummer,
                                                "user_first_name": user_first_name})  # utir i to c ho to передать dictionary


def ownCol(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    listCl = Clothes.objects.all()
    return render(request, 'clothesL/OwnCol.html',
                  {'listCl': listCl, "user_first_name": user_first_name})  # utir i to c ho to передать dictionary


def product(request, slug):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    clothes = Clothes.objects.get(slug=slug)
    commentList = 0
    comments = clothes.commentary_set.order_by('-id')[:10]
    context = {
        "object": clothes,
        "comments": comments,
        "user_first_name": user_first_name
    }
    print(clothes)
    print(comments)
    return render(request, 'clothesL/product.html', context)


@login_required
def comment(request, slug):
    try:
        a = Clothes.objects.get(slug=slug)
    except:
        raise Http404("ERROORRRRRR")

    print("request")
    print(request)
    if request.method == 'POST':
        text1 = request.POST['text']

        print(text1)
        a.commentary_set.create(author=request.user, text=text1, clothes_id=a.id)

    else:
        print()
    return HttpResponseRedirect(reverse('clothesL:product', args=(a.slug,)))


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user_first_name = None
        if self.request.user.is_authenticated:
            user_first_name = get_user_first_name(self.request.user)
        try:
            order = CartP.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'couponform': CouponForm(),
                'DISPLAY_COUPON_FORM': True,
                'user_first_name': user_first_name
            }
            return render(self.request, 'clothesL/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            print("You do not have an active order")
            return redirect("/")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class CheckSales(LoginRequiredMixin, View):
    def get(self, request):
        user_first_name = None
        if self.request.user.is_authenticated:
            user_first_name = get_user_first_name(self.request.user)
        user = self.request.user
        shoptouser = ShopToUser.objects.get(user=user.id)
        shop_id = shoptouser.shop.id
        shop = Shops.objects.get(id=shop_id)

        all = CartItemP.objects.all()
        not_all = []
        for al in all:
            if al.shop.id == shop_id:
                not_all.append(al)
        return render(request, 'clothesL/checksales.html',
                      {'all': not_all, 'shop': shop, 'user_first_name': user_first_name})


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user_first_name = None
        if self.request.user.is_authenticated:
            user_first_name = get_user_first_name(self.request.user)
        try:
            print("kirdi")
            order = CartP.objects.get(user=self.request.user, ordered=False)
            shop_order = {}
            # shops= set()
            # for i in range order
            print("in try")
            print(order)
            order_items = order.items.all()
            print('order.get_totl()', order.get_total())

            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            print(user.id)
            user_purse = Purse.get_purse_by_userid(user.id)
            shop1 = ShopToUser.get_purse_by_shop_id(1)
            shop2 = ShopToUser.get_purse_by_shop_id(2)
            print(shop1.user.id)
            shop1_purse = Purse.get_purse_by_userid(shop1.user.id)
            shop2_purse = Purse.get_purse_by_userid(shop2.user.id)
            print(shop1_purse, 'shop1')
            print(shop2_purse, 'shop2')

            shop1_money = get_user_money(shop1.user)
            print(shop2.user.username)
            shop2_money = get_user_money(shop2.user)

            added_money_shop1 = 0
            added_money_shop2 = 0
            error_message = None
            print('error', 'hello')
            with transaction.atomic():
                if user:
                    with transaction.atomic():
                        money = get_user_money(user)
                        print('shop1 money', shop1_money)
                        print('shop2 money', shop2_money)
                        print('user money', money)
                        print('money', money)
                        print('total:', order.get_total())
                        if money >= order.get_total():
                            with transaction.atomic():
                                print(order_items)
                                for order_item in order_items:
                                    # print(order_item.toString())
                                    money = money - order_item.get_final_price()
                                    print('order_item.get_final_price()', order_item.get_final_price())
                                    money_enc = (encrypt(user.id, str(money), user.username)).decode('ascii')
                                    user_purse.money = money_enc
                                    user_purse.save()
                            with transaction.atomic():
                                for order_item in order_items:
                                    if order_item.shop.id == 1:
                                        added_money_shop1 += order_item.get_final_price()
                                        shop1_money += order_item.get_final_price()
                                        print('updated shop 1', shop1_money)
                                        shop1_purse.money = (
                                            encrypt(shop1.user.id, str(shop1_money), shop1.user.username)).decode(
                                            'ascii')
                                        shop1_purse.save()
                                    elif order_item.shop.id == 2:
                                        added_money_shop2 += order_item.get_final_price()
                                        shop2_money = shop2_money + order_item.get_final_price()
                                        print('updated shop 2', shop2_money)
                                        shop2_purse.money = (
                                            encrypt(shop2.user.id, str(shop2_money), shop2.user.username)).decode(
                                            'ascii')

                                        shop2_purse.save()
                            error_message = 'Successfully transfered !!'
                        else:
                            error_message = 'Not enough money !!'
                            messages.warning(self.request, error_message)
                            return redirect("/", {'user_first_name': user_first_name})

                else:
                    error_message = 'There is no user with this email !!'

                print(error_message)

            messages.success(self.request, "Your order was successful!")
            return redirect("/main/block/transactions/new",
                            {'user_first_name': user_first_name, 'added_money_shop1': added_money_shop1,
                             'added_money_shop2': added_money_shop2})
            # return redirect("block:transactions", {'order': order})
        except:
            print("oshibka")
            messages.warning(self.request, "Yoshiibka")
            return redirect("/", {'user_first_name': user_first_name})


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = CartP.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("clothesL:order-summary")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("clothesL:order-summary")


class ItemDetailViewP(DetailView):
    model = Clothes
    template_name = "clothesL/product.html"


class PurseView(LoginRequiredMixin, View):
    def get(self, request):
        user_first_name = None
        user_email = None
        user_last_name = None
        if self.request.user.is_authenticated:
            user_first_name = get_user_first_name(self.request.user)

        user = None
        if request.user.is_authenticated:
            user = request.user
            user_email = get_user_email(user)
            user_last_name = get_user_last_name(user)
        purse = Purse.get_purse_by_userid(user.id)

        orders = CartP.objects.filter(user_id=user.id)
        data = {}
        data['user'] = user
        data['purse'] = purse
        data['money'] = get_user_money(user)
        data['user_first_name'] = user_first_name
        data['user_last_name'] = user_last_name
        data['user_email'] = user_email

        if not ShopToUser.objects.filter(user=request.user.id).exists():
            data['orders'] = orders
        print('email', user_email)
        return render(request, 'clothesL/account.html', data)


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Clothes, slug=slug)
    order_item, created = CartItemP.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
        shop=product.shop
    )
    order_qs = CartP.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            messages.info(request, "This item quantity was updated.")
            return redirect("clothesL:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("clothesL:order-summary")
    else:
        ordered_date = timezone.now()
        order = CartP.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("clothesL:order-summary")


@login_required
def remove_from_cart_p(request, slug):
    item = get_object_or_404(Clothes, slug=slug)
    order_qs = CartP.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item = CartItemP.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("clothesL:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("clothesL:order-summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("clothesL:order-summary", slug=slug)


@login_required
def remove_single_item_from_cart_p(request, slug):
    product = get_object_or_404(Clothes, slug=slug)
    order_qs = CartP.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=product.slug).exists():
            order_item = CartItemP.objects.filter(
                product=product,
                user=request.user,
                ordered=False,
                shop=product.shop
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("clothesL:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("clothesL:order-summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("clothesL:order-summary", slug=slug)


def shop_index(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    listS = Shops.objects.all()
    print(listS)
    return render(request, 'shops/all_shops.html',
                  {'listS': listS, 'user_first_name': user_first_name})  # utir i to cho to передать dictionary


def shopInfo(request, slug):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    shop = Shops.objects.get(slug=slug)
    comments = shop.commentaryshops_set.order_by('-id')[:10]
    clothes = {}
    # for i in Clothes.objects:
    #     if i.shop == shop:
    #         clothes.add(i)
    clothes = Clothes.objects.filter(shop=shop)
    context = {
        "object": shop,
        "comments": comments,
        "clothes": clothes,
        "user_first_name": user_first_name
    }
    return render(request, 'shops/shop.html', context)


@login_required
def commentsShop(request, slug):
    try:
        a = Shops.objects.get(slug=slug)
    except:
        raise Http404("ERROORRRRRR")

    if request.method == 'POST':
        text1 = request.POST['text']
        a.commentaryshops_set.create(author=request.user, text=text1, shops_id=a.id)

    else:
        pass
    return HttpResponseRedirect(reverse('clothesL:shopInfo', args=(a.slug,)))


class Blockchain(object):
    def __init__(self):
        self.chain = Block.objects.all()
        self.current_transactions = []
        self.nodes = set()

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof, previous_hash=None):
        block = Block.objects.create(
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(Block.objects.order_by("-id")[0]))
        self.current_transactions = []
        # block = {
        #     'index': len(self.chain) + 1,
        #     'timestamp': time,
        #     'transactions': self.current_transactions,
        #     'proof': proof,
        #     'previous_hash': previous_hash or self.hash(self.chain[-1]),
        # }
        # self.current_transactions = []
        # self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount, time=str(datetime.now())):
        """
        Generate new transaction information, which will be added to the next block to be mined
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'time': time
        })
        return self.last_block.id + 1

    @staticmethod
    def hash(block):
        # print(block)
        block_json = {
            'index': block.id,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
            'proof': block.proof,
            'previous_hash': block.previous_hash,
        }
        block_string = json.dumps(block_json, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def hash_dict(block):
        block_json = {
            'index': block["id"],
            'timestamp': block["timestamp"],
            'transactions': block["transactions"],
            'proof': block["proof"],
            'previous_hash': block["previous_hash"],
        }
        block_string = json.dumps(block_json, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return Block.objects.order_by("-id")[0]
        # return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof * proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5] == "00000"

    def valid_chain(self, chain):
        print(chain)

        # last_block = Block.objects.order_by("id")[0]
        current_index = 2
        last_block = chain[0]  # id=1
        print(last_block)
        while current_index < len(chain):
            # block = chain.get(id=current_index)
            # if block.previous_hash != self.hash(last_block):
            #     return False
            # # Check that the Proof of Work is correct
            # if not self.valid_proof(last_block.proof, block.proof):
            #     return False
            # last_block = block
            # current_index += 1
            try:
                for d in chain:  # d is dict
                    if d["id"] == current_index:
                        block = d  # block is dict
                        print("\n")
                        print(block)
                        print(block["previous_hash"])

                        print(last_block)
                        print(self.hash_dict(last_block))
                        print("\n")
                        if block["previous_hash"] != self.hash_dict(last_block):
                            mes = []
                            ss = "Hashes not equal!! error in block:" + str(current_index) + "\n"
                            ss += "it must be: " + block["previous_hash"] + ", not: " + self.hash_dict(last_block)

                            mes.append(ss)
                            print(mes.__str__())
                            return False, mes
                        # Check that the Proof of Work is correct
                        if not self.valid_proof(last_block["proof"], block["proof"]):
                            mes = []
                            ss = "proofs are incorrect"
                            mes.append(ss)
                            return False, mes
                        last_block = block
                        current_index += 1
            except:
                print("error in valid chain")
                mes = []
                ss = "error"
                mes.append(ss)
                return False, mes
        mes = []
        return True, mes

    def resolve_conflicts(self):
        neighbours = self.nodes
        print("hereeee")
        print(neighbours)
        new_chain = None
        max_length = len(Block.objects.all())
        mes = []
        is_replaced = False
        try:
            for node in neighbours:
                response = requests.get('http://%s/main/block/chains' % node)
                if response.status_code == 200:
                    # for obj in serializers.deserialize("json", response):
                    #     print(obj.object)
                    # length = response.json()['length']
                    # chain = response.json()['chain']
                    # Check if the length is longer and the chain is valid
                    data = response.json()
                    # print(data)
                    # print(data["length"])
                    print(data["chain"])
                    b, mes = self.valid_chain(data["chain"])

                    print('LEEEEN')
                    print(len(mes))
                    for i in mes:
                        print(i, end=" ")
                    print("\n")
                    print(b)
                    print(type(mes))
                    if not b:
                        ss = "NOW WE DO NOT TRUST " + str(node)
                        mes.append(ss)
                        self.nodes.remove(node)

                        print(''.join(mes))
                        print(mes)

                    if data["length"] >= max_length and b:
                        print("in if" + str(b))
                        max_length = data["length"]

                        for d in data["chain"]:
                            try:
                                block = Block.objects.get(id=d["id"])
                                change = 0

                                if block.id != d["id"]:
                                    block.id = d["id"]
                                    change += 1
                                if block.timestamp != d["timestamp"]:
                                    block.timestamp = d["timestamp"]
                                    change += 1
                                if block.transactions != d["transactions"]:
                                    block.transactions = d["transactions"]
                                    change += 1
                                if block.proof != d["proof"]:
                                    block.proof = d["proof"]
                                    change += 1
                                if block.previous_hash != d["previous_hash"]:
                                    block.previous_hash = d["previous_hash"]
                                    change += 1
                                block.save()
                                print(change)
                                if change > 0:
                                    is_replaced = True


                            except:
                                block = Block.objects.get_or_create(
                                    id=d["id"],
                                    timestamp=d["timestamp"],
                                    transactions=d["transactions"],
                                    proof=d["proof"],
                                    previous_hash=d["previous_hash"]
                                )
                                is_replaced = True

        except:
            print("in for")
        # Replace our chain if we discovered a new, valid chain longer than ours
        print("here is ok")

        print(''.join(mes))
        if is_replaced:
            print("True")
            ss = "Blockchain is updated!"
            mes.append(ss)
            print(''.join(mes))
            return True, mes
        if new_chain:
            print(new_chain)
            # Block.objects.all().delete()
            self.chain = new_chain
            print("true")
            return True, mes
        print("false")
        return False, mes


node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()


def mine(request, *args, **kwargs):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    last_block = blockchain.last_block
    # last_proof = last_block['proof']
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    if len(blockchain.current_transactions) == 0 and request.user.is_staff == 0:
        messages.warning(request, "you can not mine")
        return redirect("/")

    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        # 'index': block['index'],
        'index': block.id,
        # 'transactions': block['transactions'],
        'transactions': block.transactions,
        'proof': block.proof,
        # 'previous_hash': block['previous_hash']
        'previous_hash': block.previous_hash,
        # 'this_hash': blockchain.hash(blockchain.chain[-1])
        'this_hash': blockchain.hash(blockchain.last_block),
        'user_first_name': user_first_name
    }
    print(response)
    return render(request, 'block/mine.html', response)
    # return HttpResponse(json.dumps(response))


@csrf_protect
def new_transaction(request):
    # values = json.loads(request.body.decode('utf-8'))
    # required = ['sender', 'recipient', 'amount']
    # if not all(k in values for k in required):
    #     return 'Missing values'
    # index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    # print(index)
    # response = {'message': 'Transaction will be added to Block %s' % index}
    # return HttpResponse(json.dumps(response))
    # order = CartP.objects.get(user=self.request.user, ordered=False)
    # shop_order = {}
    # # shops= set()
    # # for i in range order
    # print(order)
    # order_items = order.items.all()
    # order_items.update(ordered=True)
    order = CartP.objects.get(user=request.user, ordered=False)
    cartItem = {}
    sumWoma = 0
    sumArai = 0

    order_items = order.items.all()

    # item_id = order.
    # print(order.items)
    # matches = [val for val in order.items if val in CartItemP.objects.all()]

    # for i in order_items:
    #     if i.shop_id == 1:
    #         sumWoma += i.product.priceWithProm()
    #     elif i.shop_id == 2:
    #         sumArai += i.product.priceWithProm()
    shops = {}  # shop_id: money added
    print(shops)
    print(order_items)
    for i in order_items:
        print(shops)
        if i.shop_id not in shops.keys():
            shops[i.shop_id] = i.get_final_price()
            print(shops)
            print('i:', i.get_final_price())
        else:
            shops[i.shop_id] += i.get_final_price()
            print(shops)
            print('i:', i.get_final_price())
    index = 0
    print(shops)
    for shop_id in shops:
        index = blockchain.new_transaction(request.user.username, Shops.objects.get(id=shop_id).shop_name,
                                           shops[shop_id])

    # index1 = 0
    # index2 = 0
    # index = 0
    # if sumWoma != 0:
    #     index1 = blockchain.new_transaction(request.user.username, "Woma", sumWoma)
    # if sumArai != 0:
    #     index2 = blockchain.new_transaction(request.user.username, "Arai", sumArai)
    # if index1 != 0:
    #     index = index1
    # elif index2 != 0:
    #     index = index2
    print(order)
    order_items.update(ordered=True)
    for item in order_items:
        item.save()
    order.ordered = True
    order.save()
    # response = {'message': 'Transaction will be added to Block %s' % index}
    # # return HttpResponse(json.dumps(response))
    messages.success(request, 'Transaction will be added to Block %s' % index)

    # return redirect(request, 'block/mine.html')
    return redirect("clothesL:mine")


def hashes_of_blocks():
    hashes = []
    for i in Block.objects.all():
        hashes.append(blockchain.hash(i))
    print(hashes)
    return hashes


def chains(request):
    # block_list = list(Block.objects.values())
    # return JsonResponse(block_list, safe=False)

    block_list = list(Block.objects.values())
    # block_json = serializers.serialize("json", block_list)
    # block_json = json.loads(block_list)
    response = {
        # 'chain': blockchain.chain,
        # 'length': len(blockchain.chain)
        'chain': list(block_list),
        'length': len(block_list)
    }

    return JsonResponse(response, safe=False)
    # return HttpResponse(block_json)
    # return HttpResponse(json.dumps(block_json))


def full_chain(request):
    user_first_name = None
    if request.user.is_authenticated:
        user_first_name = get_user_first_name(request.user)
    blockchain_chain = Block.objects.all()
    colors = []
    colors.append("palegreen")
    current_index = 2

    hashes_blocks = hashes_of_blocks()
    is_red = False
    while current_index <= len(blockchain_chain):

        b1 = Block.objects.get(id=current_index)
        b_prev = Block.objects.get(id=(current_index - 1))

        if blockchain.valid_proof(b_prev.proof, b1.proof) and (
                not is_red and b1.previous_hash == blockchain.hash(Block.objects.get(id=(current_index - 1)))):
            colors.append("palegreen")
        else:
            is_red = True
            colors.append("red")

        current_index += 1
    blockchain_chain2 = Block.objects.all().order_by("-id")
    colors.reverse()
    hashes_blocks.reverse()
    zippedList = zip(blockchain_chain2, hashes_blocks, colors)
    print(blockchain_chain)
    response = {
        # 'chain': blockchain.chain,
        'neighbours': blockchain.nodes,
        'length': len(blockchain_chain),
        'zip': zippedList,
        # 'hashes': hashes_of_blocks()
        'user_first_name': user_first_name
    }
    # return HttpResponse(json.dumps(response))
    print("here")
    return render(request, 'block/blockchain.html', response)


def proof_of_work(self, last_proof):
    proof = 0
    while self.valid_proof(last_proof, proof) is False:
        proof += 1
    return proof


@staticmethod
def valid_proof(last_proof, proof):
    guess = str(last_proof * proof).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:5] == "00000"


@csrf_exempt
def connect_node(request):  # New
    if request.method == 'POST':
        received_json = json.loads(request.body)
        nodes = received_json.get('nodes')
        if nodes is None:
            return "No node", HttpResponse(status=400)
        for node in nodes:
            blockchain.register_node(node)
        response = {
            'message': 'All the nodes are now connected. The Sudocoin Blockchain now contains the following nodes:',
            'total_nodes': list(blockchain.nodes)}
    return JsonResponse(response)


def replace_chain(request):  # New
    if request.method == 'GET':
        try:
            is_chain_replaced, mes = blockchain.resolve_conflicts()
            print(mes)
            try:
                if is_chain_replaced and len(mes) != 0:
                    for mess in mes:
                        messages.success(request, mess)
                elif len(mes) != 0:
                    for mess in mes:
                        messages.warning(request, mess)
                elif not is_chain_replaced:
                    messages.info(request, "All good. The chain is the largest one.")
            except:
                print("replace chain")

        except:
            print("replace chain error")
    return redirect("clothesL:chain")


class ClothesCreateView(generics.CreateAPIView):
    serializer_class = ClothesDetailSerializer


class ClothesOnlyShopView(generics.CreateAPIView):
    serializer_class = ClothesOnlyShopSerializer


class ClothesListView(generics.ListAPIView):
    serializer_class = ClothesListSerializer
    queryset = Clothes.objects.all()


class CouponCreateView(generics.CreateAPIView):
    serializer_class = CouponDetailSerializer


class ShopsCreateView(generics.CreateAPIView):
    serializer_class = ShopsDetailSerializer


class ClothesDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ClothesDetailSerializer
    queryset = Clothes.objects.all()
# if data["length"] > max_length and b:
#     print("in if")
#     max_length = data["length"]
#     for d in data["chain"]:
#         block = Block.objects.get_or_create(
#             id=d["id"],
#             timestamp=d["timestamp"],
#             transactions=d["transactions"],
#             proof=d["proof"],
#             previous_hash=d["previous_hash"]
#         )
