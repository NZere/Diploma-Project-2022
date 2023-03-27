from django.shortcuts import render
from django.shortcuts import render
from .models import Shops
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.


def index(request):
    listS = Shops.objects.all()
    print(listS)
    return render(request, 'shops/all_shops.html', {'listS': listS})  # utir i to cho to передать dictionary


def shopInfo(request, slug):
    shop = Shops.objects.get(slug=slug)
    comments = shop.commentary_set.order_by('-id')[:10]
    context = {
        "object": shop,
        "comments": comments,
        "clothes": clothes
    }
    return render(request, 'shops/shop.html', context)

@login_required
def comment(request, slug):
    try:
        a = Shops.objects.get(slug=slug)
    except:
        raise Http404("ERROORRRRRR")

    if request.method == 'POST':
        text1 = request.POST['text']
        a.commentary_set.create(author=request.user, text=text1, shop_id=a.id)

    else:
        pass
    return HttpResponseRedirect(reverse('main:product', args=(a.slug,)))