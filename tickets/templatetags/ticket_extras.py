import arrow
from django import template

register = template.Library()


@register.filter
def get_total_ticket_comments(ticket):
    total_comments = 0
    for comment in ticket.comments.all():
        total_comments += ticket.comments.count()
    return total_comments


@register.filter
def started_time(created_date):
    return arrow.get(created_date).humanize()


@register.simple_tag
def last_comment_user_name(ticket):
    comments = ticket.comments.all().order_by('created_date')
    return comments[comments.count()-1].user.username


@register.simple_tag
def last_comment_user(ticket):
    comments = ticket.comments.all().order_by('created_date').last()
    name = comments.user.first_name + " " + comments.user.last_name
    return name


@register.simple_tag
def last_comment_date(ticket):
    comments = ticket.comments.all().order_by('created_date')
    return arrow.get(comments[comments.count()-1].created_date).humanize()


@register.simple_tag
def comment_date_humanized(comment):
    return arrow.get(comment.created_date).humanize()




