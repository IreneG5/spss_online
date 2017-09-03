# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django import template
from products.models import Purchase

register = template.Library()


@csrf_exempt
def paypal_return(request):
    time.sleep(10) # Wait a bit for paypal to send the signal
    last_purchase = Purchase.objects.last()
    args = {'post': request.POST, 'get': request.GET, 'last_purchase': last_purchase}
    return render(request, 'paypal/paypal_return.html', args)


def paypal_cancel(request):
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'paypal/paypal_cancel.html', args)

