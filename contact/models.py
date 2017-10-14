# -*- coding: utf-8 -*-
from django.db import models


class Contact(models.Model):
    """
    Contact are queries that visitors or customers send to easySPSS.
    They are not linked to users as there is no need to be registered or logged in to fill out the form.
    """

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(blank=False, null=False)
    query = models.TextField(max_length=255)

    def __unicode__(self):
        return '%s - %s' % (self.email, self.pk)
