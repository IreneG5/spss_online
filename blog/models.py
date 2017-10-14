# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='blog')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='blog')
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to="blogimage/", blank=True, null=True)
    score = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes')
    post = models.ForeignKey(Post, related_name='votes')
    vote = models.IntegerField(default=0)

    def __unicode__(self):
        return '%d-%s' % (self.pk, self.post.title)

