# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib import messages
from django import template
from products.models import Purchase, PurchaseTemp

register = template.Library()


@csrf_exempt
def paypal_return(request):
    """
        Workaround for PayPay issue getting 3 signals
        1. PayPal purchases from signals are being saved in PurchasesTemp with some delays
        2. Wait for until a minute to read the PurchaseTemp when it's saved
        3. Take the last saved and save it in Purchase table
        4. Wait until the 3 PurchaseTemp are saved and empty the table.
    """
    # Check when the PurchaseTemp is being saved in the DB
    count = 0
    while count < 3:
        if PurchaseTemp.objects.last()is None:
            count += 1
            print count
            time.sleep(3)
        else:
            count = 99
            print "Found"

    # If it was saved, copy it in the Purchase table and empty PurchaseTemp table
    if count == 99:
        print("Saving purchase")
        last_purchase_temp = PurchaseTemp.objects.last()
        Purchase.objects.create(product_id=last_purchase_temp.product.id, user_id=last_purchase_temp.user_id,
                            license_end=last_purchase_temp.license_end)
        num_temp=PurchaseTemp.objects.all().count()
        while num_temp<3:
            print num_temp
            time.sleep(3)
            num_temp = PurchaseTemp.objects.all().count()

        PurchaseTemp.objects.all().delete()
        args = {'post': request.POST, 'get': request.GET, 'last_purchase': last_purchase_temp}
        return render(request, 'paypal/paypal_return.html', args)
    # If no purchase was found, send an error
    else:
        print("Not found")
        messages.error(request, "We were unable to save your purchase", extra_tags='alert alert-danger')
        args = {'post': request.POST, 'get': request.GET}
        return render(request, 'paypal/paypal_return.html', args)


# Original function
# def paypal_return(request):
  #   last_purchase = Purchase.objects.last()
  #   args = {'post': request.POST, 'get': request.GET, 'last_purchase': last_purchase}
  #   return render(request, 'paypal/paypal_return.html'



def paypal_cancel(request):
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'paypal/paypal_cancel.html', args)

