from django.urls import path
from . import views
from django.views.generic import ListView, DetailView


app_name = 'shops'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug>/', views.shopInfo, name='shopInfo'),

]













































# path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
# path('request-refund/', RequestRefundView.as_view(), name='request-refund')