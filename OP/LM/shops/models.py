from django.db import models

from django.shortcuts import reverse

# from LM.main.models import Clothes


class Shops(models.Model):
    shop_name = models.CharField('ShopName', max_length=100)
    text = models.TextField('Text')
    logo_shop = models.ImageField(upload_to="media/shop_image", blank=True)
    website = models.CharField('Website', max_length=100)
    slug = models.SlugField(default=shop_name)


class CommentaryShops(models.Model):
    author = models.CharField('Author', max_length=100)
    text = models.TextField('Text')
    shops = models.ForeignKey(Shops, on_delete=models.CASCADE)

    def get_add_to_cart_url(self):
        return reverse("shops:comment", kwargs={
            'slug': self.shops.slug
        })
