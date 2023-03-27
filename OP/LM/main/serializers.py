from rest_framework import serializers
from .models import Clothes, Coupon, Shops


class ClothesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = '__all__'


class ClothesOnlyShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ('id', 'shop_id', 'price')



class ClothesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ('shop', 'price','image')


class CouponDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class ShopsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = '__all__'
