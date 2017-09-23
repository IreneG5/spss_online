# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Ticket, Comment


# Register your models here.
admin.site.register(Ticket)
admin.site.register(Comment)

