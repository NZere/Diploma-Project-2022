from django.urls import path, re_path
from . import views
from django.views.generic import ListView, DetailView
from .models import Clothes
from .views import (
    ItemDetailViewP,
    # ItemDetailViewK,
    # CheckoutView,
    OrderSummaryView,
    add_to_cart,
    # add_to_cartK,
    remove_from_cart_p,
    remove_single_item_from_cart_p,
    PaymentView,
    AddCouponView,
    # RequestRefundView
    ClothesCreateView,
    CouponCreateView,
    ShopsCreateView,
    ClothesDetailView,
    ClothesListView,
    CheckSales,
    ClothesOnlyShopView,

)

app_name = 'main'
urlpatterns = [
    path('collection/', views.index, name='index'),
    path('collection/men/', views.men, name='men'),
    path('collection/women/', views.women, name='women'),
    path('collection/prom/', views.prom, name='prom'),
    path('collection/blog/', views.blog, name='blog'),
    path('collection/winter/', views.winter, name='winter'),
    path('collection/school/', views.school, name='school'),
    path('collection/oscar/', views.oscar, name='oscar'),
    path('collection/dress/', views.dress, name='dress'),
    path('collection/summerCol/', views.summerCol, name='summerCol'),
    path('collection/winterCol/', views.winterCol, name='winterCol'),
    path('collection/ownCollection/', views.ownCol, name='ownCol'),
    path('collection/newCollection/', views.newCol, name='newCol'),
    path('collection/order-summary/', OrderSummaryView.as_view(), name='order-summary'),  ####cart
    path('collection/product/people/<slug>/', views.product, name='product'),
    path('collection/add-to-cart/people/<slug>/', add_to_cart, name='add-to-cart-p'),
    path('collection/add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('collection/remove-from-cart/<slug>/', remove_from_cart_p, name='remove-from-cart-p'),
    path('collection/remove-item-from-cart/<slug>/', remove_single_item_from_cart_p,
         name='remove-single-item-from-cart-p'),

    path('collection/comment/<slug>/', views.comment, name='comment-p'),
    path('collection/payment/', PaymentView.as_view(), name='payment'),
    path('collection/shops/', views.shop_index, name='shop_index'),
    path('collection/shops/<slug>/', views.shopInfo, name='shopInfo'),
    path('collection/commentShop/<slug>/', views.commentsShop, name='comment-shop'),
    path('collection/account/', views.PurseView.as_view(), name='account'),
    path('collection/checksales', views.CheckSales.as_view(), name='checksales'),

    re_path(r'block/mine', views.mine, name='mine'),
    re_path(r'block/transactions/new/', views.new_transaction, name='transactions'),
    re_path(r'block/chain/', views.full_chain, name='chain'),
    re_path(r'block/chains/', views.chains, name='chains'),
    re_path(r'block/connect', views.connect_node, name='connect-node'),
    re_path(r'block/replace', views.replace_chain, name='replace'),

    path('api/clothes/create', ClothesCreateView.as_view()),
    path('api/clothes/all', ClothesListView.as_view()),
    path('api/coupon/create', CouponCreateView.as_view()),
    path('api/shops/create', ShopsCreateView.as_view()),
    path('api/clothes/detail/<int:pk>', ClothesDetailView.as_view()),
    path('api/clothes/createShop', ClothesOnlyShopView.as_view()),

]

# path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
# path('request-refund/', RequestRefundView.as_view(), name='request-refund')
