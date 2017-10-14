# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import arrow
from django.shortcuts import render
from .models import Product, Purchase


# Create your views here.
def all_products(request):
    products = Product.objects.all().order_by('-name')
    today = arrow.now() # passed as argument to compare the products with an active licence in the template
    expire_soon = arrow.now().replace(days=+30).datetime  # passed as argument to highlight the products close to expire
    purchases = Purchase.objects.filter(user_id=request.user.id).order_by('license_end')
    args = {'products': products, 'purchases': purchases, 'today': today, 'expire_soon': expire_soon}
    return render(request, "products/products.html", args)


