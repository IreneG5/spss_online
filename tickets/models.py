# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings


class Ticket(models.Model):
    """
    Tickets are support cases that active customers can log to get help.
    Each ticket contains its own fields and is associated to an user and
    a particular product which customer license
    has to be active at the time of the creation of the ticket.
    The owner of the ticket needs to be a customer in order for the
    customer to see it in the "My Tickets" section.
    Tickets can be opened on the site or from the admin panel.
    """
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='tickets')
    status = models.CharField(max_length=50, choices=statuses,
                              default='NEW')
    reason = models.CharField(max_length=50, choices=reasons,
                              default='OTH')
    product = models.ForeignKey('products.Product',
                                related_name='tickets')
    opened_date = models.DateTimeField(default=timezone.now)
    closed_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.subject, self.user.email)


class Comment(models.Model):
    """
    Comments are the way users and staff communicate in tickets.
    Each ticket must contain at least one comment.
    Each comment is associated to a ticket and a user.
    If a ticket is created in the admin panel, a comment associated
    to it should be created immediately after.
    Comments can be created on the site or from the admin panel.
    """
    ticket = models.ForeignKey(Ticket, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments')
    comment = HTMLField()
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s - ticket:%s - %s' % (self.pk, self.ticket_id, self.user)
