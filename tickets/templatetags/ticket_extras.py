import arrow
from django import template

register = template.Library()


@register.filter
def get_total_ticket_comments(ticket):
    """ Return the total number of comments for the given ticket """

    total_comments = 0
    for comment in ticket.comments.all():
        total_comments += comment.count()
    return total_comments


@register.simple_tag
def last_comment_user(ticket):
    """ Return the full name of the user that looged the last comment on the given ticket """

    comments = ticket.comments.all().order_by('created_date').last()
    name = comments.user.first_name + " " + comments.user.last_name
    return name


@register.simple_tag
def last_comment_date(ticket):
    """
    Get the comments associated to the given ticket and
    return a visual representation of the date of the last one
    """

    comments = ticket.comments.all().order_by('created_date')
    return arrow.get(comments[comments.count()-1].created_date).humanize()


@register.simple_tag
def comment_date_humanized(comment):
    """ Return a more visual representation of the date given """

    return arrow.get(comment.created_date).humanize()

