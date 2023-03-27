import datetime
from django.db import models
from django.utils import timezone
import django
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User, auth


class Shops(models.Model):
    shop_name = models.CharField('ShopName', max_length=100)
    text = models.TextField('Text')
    logo_shop = models.ImageField(upload_to="media/shop_image", blank=True)
    website = models.CharField('Website', max_length=100)
    slug = models.SlugField(default=shop_name)


class ShopToUser(models.Model):
    shop = models.OneToOneField(Shops, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @staticmethod
    def get_purse_by_shop_id(shop_id):
        return ShopToUser.objects.get(shop=shop_id)


class CommentaryShops(models.Model):
    author = models.CharField('Author', max_length=100)
    text = models.TextField('Text')
    shops = models.ForeignKey(Shops, on_delete=models.CASCADE)

    def get_add_to_cart_url(self):
        return reverse("shops:comment", kwargs={
            'slug': self.shops.slug
        })


class Clothes(models.Model):
    boolOff = models.BooleanField(default="False")
    boolUp = models.BooleanField(default="False")
    boolDown = models.BooleanField(default="False")
    boolOutwear = models.BooleanField(default="False")
    boolShoes = models.BooleanField(default="False")
    boolAcc = models.BooleanField(default="False")
    name = models.CharField(max_length=100)
    genderW = models.BooleanField(default=False)
    genderM = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    prom = models.FloatField(default=0)
    date = models.DateTimeField(default=django.utils.timezone.now)
    image = models.ImageField(upload_to="media/clothes_image", blank=True)
    slug = models.SlugField(default=name)
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE)

    def isProm_0(self):
        if (self.prom == 0):
            return True
        else:
            return False

    def priceWithProm(self):
        price = self.price-self.price / 100 * self.prom
        return price

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("mainApp:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart-p", kwargs={
            'slug': self.slug
        })

    def get_product(self):
        return reverse("main:product", kwargs={
            'slug': self.slug
        })

    def leave_comment(self):
        return reverse("main:comment-p", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart-p", kwargs={
            'slug': self.slug
        })

    def was_published_recently(self):
        return self.date >= (timezone.now() - datetime.timedelta(days=14))


class CartItemP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE)

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.priceWithProm()

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        print('final', self.get_total_discount_item_price())
        return self.get_total_discount_item_price()

    def __unicode__(self):
        return "Cart item for product (People)" + self.product.name
    # def toString(self):
    #     return self.user.name+" "+self.product.name+" "+self.g+self.get_total_item_price()



class CartP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    items = models.ManyToManyField(CartItemP)
    start_date = models.DateTimeField(auto_now_add=True)  # auto_now_add=True,
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.CASCADE, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            a = order_item.product.price - (order_item.product.prom / 100 * order_item.product.price)
            print(a)
            b = order_item.quantity * a
            total += b

        if self.coupon:
            total = total - (self.coupon.amount) / 100 * total

        return total


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Commentary(models.Model):
    author = models.CharField('Author', max_length=100)
    text = models.TextField('Text')
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)

    def get_add_to_cart_url(self):
        return reverse("main:comment-p", kwargs={
            'slug': self.clothes.slug
        })

class Block(models.Model):
    timestamp = models.TextField(default=datetime.date.today())
    transactions = models.TextField('Transactions')
    proof = models.IntegerField()
    previous_hash = models.TextField('Hash')


class Purse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    money = models.TextField()

    @staticmethod
    def get_purse_by_userid(user_id):
        return Purse.objects.get(user=user_id)
