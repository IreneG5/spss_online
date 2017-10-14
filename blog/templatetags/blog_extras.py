from django import template
from ..models import Post

register = template.Library()


# Get the 3 posts with higher score
@register.inclusion_tag('blog/most_voted_posts.html')
def get_most_voted_posts():
        posts = Post.objects.all().order_by('-score')[:3]
        print posts
        return {'posts': posts}


# Get the 3 posts with higher number of views
@register.inclusion_tag('blog/most_viewed_posts.html')
def get_most_viewed_posts():
        posts = Post.objects.all().order_by('-views')[:3]
        print posts
        return {'posts': posts}

