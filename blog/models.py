# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    """ Each blog post belongs to a pre-defined category.
    Categories are set up on the admin panel """

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    """
    Each blog post contains its own fields and is liked to a user (author) and to a category.
    Blog posts are created on the admin panel
    Score is calculated on the post_voteup and post_votedown views when the user vote on the post_detail page
    Views are incremented on the post_detail view every time the post_detail template is rendered
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='blog')
    image = models.ImageField(upload_to="blogimage/", blank=True, null=True)
    views = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title


class Vote(models.Model):
    """
    Votes for blog posts are stored in a different model to avoid a user voting multiple times.
    Votes are linked to users and posts, allowing only one vote per user per post.
    The vote value is saved on the post_voteup and post_votedown views when the user vote on the post_detail page
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes')
    post = models.ForeignKey(Post, related_name='votes')
    vote = models.IntegerField(default=0)

    def __unicode__(self):
        return '%d-%s' % (self.pk, self.post.title)
