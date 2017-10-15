# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import timezone
from .models import Post, Vote


def post_list(request):
    """ Return a list with all published posts sorted by published date. """

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "blog/blog_posts.html", {'posts': posts})


def post_detail(request, post_id):
    """ Take a post id and return the post details. Increment views every time the post template is rendered."""

    post = get_object_or_404(Post, pk=post_id)
    post.views += 1
    post.save()

    # Needed to share post in tweeter
    current_path = "http://spss-online.herokuapp.com%s" % request.get_full_path()
    args = {'post': post, 'current_path': current_path}

    return render(request, "blog/post_detail.html", args)


def post_voteup(request, post_id):
    """ Take a post id, check if the user has already voted, if it hasn't, register the vote and increase the post score.
    Return to the post detail template with the new score and a message """

    user = request.user
    user_post_vote = Vote.objects.filter(post_id=post_id).filter(user_id=user.id)
    # Check if the user has already voted in this post
    if user_post_vote:
        messages.success(request, "You have already voted in this post", extra_tags='alert alert-danger')
    else:
        post = get_object_or_404(Post, pk=post_id)
        vote = Vote(post=post, user=user, vote=1)
        vote.save()
        post.score += 1
        post.save()
        messages.success(request, "Your vote has been logged", extra_tags='alert alert-success')

    return redirect(reverse('post-detail', args={post_id}))


# After a user vote down, this view take the user back to the post detail with the new vote count and a message
def post_votedown(request, post_id):
    """ Take a post id, check if the user has already voted, if it hasn't, register the vote and decrease the post score.
        Return to the post detail template with the new score and a message """
    user = request.user
    user_post_vote = Vote.objects.filter(post_id=post_id).filter(user_id=user.id)

    # Check if the user has already voted in this post
    if user_post_vote:
        messages.success(request, "You have already voted in this post", extra_tags='alert alert-danger')
    else:
        post = get_object_or_404(Post, pk=post_id)
        vote = Vote(post=post, user=user, vote=-1)
        vote.save()
        post.score -= 1
        post.save()
        messages.success(request, "Your vote has been logged", extra_tags='alert alert-success')

    return redirect(reverse('post-detail', args={post_id}))
