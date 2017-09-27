# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings


# Create your models here.
class Ticket(models.Model):
    statuses = (
        ('NEW', 'New'),
        ('PCR', 'Pending Customer Response'),
        ('PER', 'Pending easySPSS Response'),
        ('CLS', 'Closed'),
    )

    reasons = (
        ('DWL', 'Download Issue'),
        ('INS', 'Installation/Licensing Issue'),
        ('SWI', 'Software Issue'),
        ('OTH', 'Other'),
    )

    subject = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets')
    status = models.CharField(max_length=50, choices=statuses, default='NEW')
    reason = models.CharField(max_length=50, choices=reasons, default='OTH')
    # I want to show only the products that the user have an active license
    product = models.ForeignKey('products.Product', related_name='tickets')
    opened_date = models.DateTimeField(default=timezone.now)
    closed_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' %(self.subject, self.user.email)


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')
    comment = HTMLField()
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s - ticket:%s - %s' %(self.pk, self.ticket_id, self.user)

