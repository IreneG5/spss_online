# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import arrow
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import auth, messages
from django import template
from products.models import Purchase
from accounts.models import User

register = template.Library()


@csrf_exempt
@login_required(login_url='/login/')
def paypal_return(request):
    """
    Render paypal_return.html template when the purchase through paypal finish successfully (on PayPal side).
    Every second (up to 15 seconds)retrieve the last purchase and compare it with the current date to
    see if it was made in the last 3 minutes (enough time for paypal to send the signal
    and the user to come back to the merchant's page) as it could be getting a previous purchase.
    If last purchase is found (the user has at least one purchase) and it was in the last 3 minutes,
    it renders the page with the recent purchase information, otherwise it shows an error message.
    """

    if User.is_authenticated:
        user = auth.get_user(request)
        # Check every second (up to 15 seconds) if the purchase was saved in case the PayPal signal is delayed
        not_found = 0

        while not_found < 15:
            # Retrieve the last_purchase from the user
            last_purchase = Purchase.objects.filter(user_id=user).last()
            # If the user has at least one purchase (last_purchase exists)
            if last_purchase:
                # Calculate when the purchase was made from the license_end field
                year = last_purchase.license_end.year - int(last_purchase.product.license_type[0])
                last_purchase_date = last_purchase.license_end.replace(year=year)
                # If this purchase was made in the last 3 minutes this is what we are looking form
                # The 3 minutes it to give Paypal time to send the signal and the user to come back to
                # the website.
                if last_purchase_date >= arrow.utcnow().replace(seconds=-180).datetime:
                    break
            not_found += 1
            time.sleep(1)

        # If a purchase made within the last 3 minutes couldn't be found, show an error message.
        if not_found == 15:
            messages.error(request, "There was a problem retrieving your purchase.",
                           extra_tags='alert alert-danger')
            args = {'html': "Please refresh the page. "
                            "If the problem persists contact PayPal for further assistance."}
        # If a purchase made within the last 3 minutes was found, it returns the details to the page.
        else:
            args = {'post': request.POST, 'get': request.GET, 'last_purchase': last_purchase}

    else:
        messages.error(request, "You are not logged in.", extra_tags='alert alert-danger')
        args = {'html': "Only logged users can see their last purchase right after the transaction is made."}

    return render(request, 'paypal/paypal_return.html', args)


@login_required(login_url='/login/')
def paypal_cancel(request):
    """ Render paypal_cancel.html template when the user click cancel during a purchase process in PayPal."""

    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'paypal/paypal_cancel.html', args)

