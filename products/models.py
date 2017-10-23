# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from paypal.standard.ipn.signals import valid_ipn_received
from django.utils import timezone
from signals import subscription_created

# Types of licenses for the license_type field in Product
license_types = (
    ('1 year', '1'),
    ('2 years', '2'),
)


class Product(models.Model):
    """
    Store the products of the company.
    Products are created in the admin panel.
    Products have no relation with any other Model
    """

    code = models.CharField(max_length=20, default="")
    name = models.CharField(max_length=100, default="")
    osystem = models.CharField(max_length=10, default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    license_type = models.CharField(max_length=50, choices=license_types,
                                    default='1')
    image = models.ImageField(upload_to="productimage/", blank=True, null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)


class Purchase (models.Model):
    """
    Store the purchases made by the user through PayPal.
    Purchases have a one to many relation with Products and Users models.
    Calculate when the license will expire depending on the type of
    license bought.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='purchases')
    product = models.ForeignKey(Product)
    license_end = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s - %s' % (self.product.name, self.user.email)


# Listen form the Paypal ipn signal
valid_ipn_received.connect(subscription_created)
