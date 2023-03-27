from django.contrib import admin
from .models import Clothes, CartItemP, CartP, Commentary, Coupon, Shops, CommentaryShops, Purse

admin.site.register(Purse)
admin.site.register(Shops)
admin.site.register(CommentaryShops)
admin.site.register(Clothes)
admin.site.register(CartItemP)
admin.site.register(CartP)
admin.site.register(Commentary)
admin.site.register(Coupon)
