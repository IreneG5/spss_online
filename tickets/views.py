# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.utils import timezone
from .forms import TicketForm, CommentForm
from tickets.models import Comment, Ticket
from products.models import Purchase, Product
from django.core.mail import send_mail

""" All views rendering templates are for authenticated users only"""


@login_required(login_url='/login/')
def tickets_list(request):
    """
    Show tickets page
    Return a list with the relevant tickets for the user
    authenticated to the ticket_list template.
    - If the user is staff: return all tickets
    - If the user is customer/registered: return its own tickets
    """

    user = request.user
    if user.is_staff:
        # Get list of all tickets for staff user
        tickets = Ticket.objects.all().order_by('-opened_date')
        comments = Comment.objects.all()
        for ticket in tickets:
            if comments.count() > 1 and ticket.status != 'CLS':
                update_pending_status(request, ticket)
    else:
        # Get list of tickets for the logged user
        tickets = Ticket.objects.filter(user_id=user.id)\
            .order_by('-opened_date')
        comments = Comment.objects.filter(user_id=user.id)

    args = {'tickets': tickets, 'comments': comments}
    return render(request, 'tickets/tickets_list.html', args)


@login_required(login_url='/login/')
def ticket_detail(request, ticket_id):
    """
    Show ticket detail page.
    Get the ticket with the id passed and return a the details
    and comments associated with that ticket
    to the ticket_detail template
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    comments = Comment.objects.filter(ticket_id=ticket_id)\
        .order_by('created_date')
    if comments.count() > 1 and ticket.status != 'CLS':
        update_pending_status(request, ticket)

    args = {'ticket': ticket, 'comments': comments}
    args.update(csrf(request))
    return render(request, 'tickets/ticket_detail.html', args)


@login_required(login_url='/login/')
def new_ticket(request):
    """
    Register a new ticket and comment.
    Show the new ticket and new comment forms and save the
    objects when both forms are validated.
    Tickets are associated to active product licenses when created.
    Only active licenses are showed in the dropdown.
    """

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        user_purchases = Purchase.objects.filter(user=request.user)
        active_purchases = Purchase.objects.filter(license_end__gte=timezone.now())
        purchases = user_purchases & active_purchases
        active_products = [purchase.product_id for purchase in purchases]
        ticket_form.fields['product'].queryset = Product.objects\
            .filter(pk__in=active_products)
        comment_form = CommentForm(request.POST)

        if ticket_form.is_valid() and comment_form.is_valid():
            ticket = ticket_form.save(False)
            ticket.user = request.user
            ticket.save()

            comment = comment_form.save(False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            messages.success(request, "Your ticket has been logged.\n"
                                      "We will send you an email"
                                      "when you get a new response.",
                             extra_tags='alert alert-success')
            return redirect(reverse('ticket-detail', args={ticket.pk}))

    else:
        ticket_form = TicketForm()
        # Set up the list of products so it only shows
        # the active products for the user
        user_purchases = Purchase.objects.filter(user=request.user)
        active_purchases = Purchase.objects\
            .filter(license_end__gte=timezone.now())
        purchases = user_purchases & active_purchases
        active_products = [purchase.product_id for purchase in purchases]
        ticket_form.fields['product'].queryset = Product.objects\
            .filter(pk__in=active_products)

        comment_form = CommentForm(request.POST)

    args = {'ticket_form': ticket_form, 'comment_form': comment_form}
    args.update(csrf(request))

    return render(request, 'tickets/ticket_form.html', args)


@login_required(login_url='/login/')
def new_comment(request, ticket_id):
    """
    Register a new comment in a given ticket.
    Get the ticket associated with the id passed,
    show new comment form and save the comment when the form is validated
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been logged",
                             extra_tags='alert alert-success')
            if comment.user.is_staff:
                send_email_comment(request, ticket, comment)

            return redirect(reverse('ticket-detail', args={ticket.pk}))
    else:
        comment_form = CommentForm(request.POST)
        args = {
            'comment_form': comment_form,
            'form_action': reverse('new-comment', args=[ticket_id]),
            'button_text': 'Add Comment',
            'ticket_id': ticket_id
        }

        args.update(csrf(request))
        return render(request, 'tickets/comment_form.html', args)


def update_pending_status(request, ticket):
    """
    Function to update status depending on last commented user.
    Get the last comment of the ticket and update the
    ticket status in concordance:
     Pending Customer Response (PCR) if the last comment was from a staff user
     and Pending easySPSS Reponse (PER) if the last comment was from a customer
     """

    last_comment = ticket.comments.all().order_by('created_date').last()
    if last_comment.user.is_staff:
        ticket.status = "PCR"
    else:
        ticket.status = "PER"
    ticket.save()


def close_ticket(request, ticket_id):
    """
    Close an open ticket.
    Change the ticket status to closed and return to ticket detail page
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.status = "CLS"
    ticket.closed_date = timezone.now()
    ticket.save()
    messages.success(request, "The ticket has been closed",
                     extra_tags='alert alert-success')
    return redirect(reverse('ticket-detail', args={ticket_id}))


def reopen_ticket(request, ticket_id):
    """
    Reopen a closed ticket
    Change the ticket status depending on the last comment
    and return to ticket detail page
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    update_pending_status(request, ticket)
    ticket.closed_date = None
    ticket.save()
    messages.success(request, "The ticket has been re-opened",
                     extra_tags='alert alert-success')
    return redirect(reverse('ticket-detail', args={ticket_id}))


def delete_comment(request, ticket_id, comment_id):
    """
    Delete a comment.
    Get the comment, delete it and return to ticket detail page
    """

    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    messages.success(request, "The comment was deleted!",
                     extra_tags='alert alert-success')

    return redirect(reverse('ticket-detail', args={ticket_id}))


def send_email_comment(request, ticket, comment):
    """
    Send email to user.
    Send a notification email to the user when a staff member
    adds a new comment.
    """
    subject = "New comment in ticket: %s" % ticket.subject
    message = "Hi %s,\n\n" \
              "A new comment has been added to ticket '%s'.\n\n" \
              "You can see the details in 'My Tickets':" \
              "https://spss-online.herokuapp.com/tickets/%s\n\n"\
              "Kind regards,\n easySPSS Team"\
              % (comment.user.first_name, ticket.subject, ticket.id)

    from_email = "easyspssweb@gmail.com"
    send_mail(subject, message, from_email, [ticket.user.email])
