from django import template
from ..models import Post

register = template.Library()


@register.inclusion_tag('blog/most_voted_posts.html')
def get_most_voted_posts():
    """ Return a list with the 3 posts with higher score """
    posts = Post.objects.all().order_by('-score')[:3]
    print posts
    return {'posts': posts}


@register.inclusion_tag('blog/most_viewed_posts.html')
def get_most_viewed_posts():
    """ Return a list with the 3 posts with higher number of views """
    posts = Post.objects.all().order_by('-views')[:3]
    print posts
    return {'posts': posts}
