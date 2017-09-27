# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import arrow
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib import auth, messages
from django import template
from products.models import Purchase
from accounts.models import User

register = template.Library()


@csrf_exempt
def paypal_return(request):
    # Check that the last purchase for the user logged in was saved in the last 3 minutes
    # (to give the user time to return to the Merchant's website)
    if User.is_authenticated:
        user = auth.get_user(request)
        last_purchase = Purchase.objects.filter(user_id=user).last()
        year = last_purchase.license_end.year - int(last_purchase.product.license_type[0])
        last_purchase_date = last_purchase.license_end.replace(year=year)

        print user.id
        print last_purchase.user_id
        print last_purchase_date
        print arrow.utcnow().replace(seconds=-180).datetime

        # Check every 3 seconds (up to 30 seconds) if the purchase was saved in case there PayPal signal is delayed
        not_found = 0
        while not_found < 10: # 10 for production
            if last_purchase_date < arrow.utcnow().replace(seconds=-180).datetime:
                not_found += 1
                # print not_found
                time.sleep(3)
            else:
                # print "Found"
                break

        if not_found == 10:

            messages.error(request, "There was a problem retrieving your purchase.",
                           extra_tags='alert alert-danger')
            args = {'html': "Please refresh the page. "
                            "If the problem persists contact PayPal for further assistance"}
        else:
            args = {'post': request.POST, 'get': request.GET, 'last_purchase': last_purchase}

    else:
        messages.error(request, "You are not logged in.", extra_tags='alert alert-danger')

        args = {'html': "Only logged users can see their last purchase right after the transaction is made."}

    return render(request, 'paypal/paypal_return.html', args)


def paypal_cancel(request):
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'paypal/paypal_cancel.html', args)

