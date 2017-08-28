# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received
from django.utils import timezone
from signals import subscription_created, subscription_was_cancelled


license_types=(
    ('1 year', '12'),
    ('2 years', '24'),
    ('perpetual', '999999'),
)


# Create your models here.
class Product(models.Model):
    code = models.CharField(max_length=20, default="")
    name = models.CharField(max_length=100, default="")
    osystem = models.CharField(max_length=10, default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    license_type = models.CharField(max_length=50, choices=license_types, default="1 year")

    # Passes the info needed for the PaypalPaymentForm to create
    # the button and required HTML when we render the template
    # Only used for Paypal individual payments. Remove if not used
    @property
    def paypal_form(self):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": self.price,
            "currency": "EUR",
            "item_name": "%s-%s" % (self.pk, uuid.uuid4()),
            "notify_url": settings.PAYPAL_NOTIFY_URL,
            "return_url": "%s/paypal-return/" % settings.SITE_URL,
            "cancel_return": "%s/paypal-cancel/" % settings.SITE_URL
        }

        return PayPalPaymentsForm(initial=paypal_dict)

    def __unicode__(self):
        return self.name


class Purchase (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchases')
    product = models.ForeignKey(Product)
    license_end = models.DateTimeField(default=timezone.now)


valid_ipn_received.connect(subscription_created)
valid_ipn_received.connect(subscription_was_cancelled)