# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import arrow
from django.shortcuts import render
from .models import Product, Purchase


# Create your views here.
def all_products(request):
    products = Product.objects.all()
    today = arrow.now()
    purchases = Purchase.objects.filter(user_id=request.user.id).order_by('-license_end')
    args = {'products':products, 'purchases':purchases, 'today':today}
    return render(request, "products/products.html", args)



