# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.utils import timezone
from .forms import TicketForm, CommentForm
from tickets.models import Comment, Ticket
from products.models import Purchase, Product


# Create your views here.
@login_required()
def tickets_list(request):
    # Get list of tickets for the logged user
    tickets = Ticket.objects.filter(user_id=request.user.id).order_by('-opened_date')
    comments = Comment.objects.filter(user_id=request.user.id)
    args = {'tickets': tickets, 'comments': comments}
    return render(request, 'tickets/tickets_list.html', args)


@login_required()
def ticket_detail(request, ticket_id):
    # Get details of specific ticket with list of comments
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    comments = Comment.objects.filter(ticket_id=ticket_id).order_by('-created_date')
    args = {'ticket': ticket, 'comments': comments}
    args.update(csrf(request))
    return render(request, 'tickets/ticket_detail.html', args)


@login_required()
def new_ticket(request):
    # Create new ticket
    if request.method=='POST':
        ticket_form = TicketForm(request.POST)
        user_purchases = Purchase.objects.filter(user=request.user)
        active_purchases = Purchase.objects.filter(license_end__gte=timezone.now())
        purchases = user_purchases & active_purchases
        active_products = [purchase.product_id for purchase in purchases]
        ticket_form.fields['product'].queryset = Product.objects.filter(pk__in=active_products)
        comment_form = CommentForm(request.POST)

        if ticket_form.is_valid() and comment_form.is_valid():
            ticket = ticket_form.save(False)
            ticket.user = request.user
            print "TICKET"
            print ticket
            print ticket.product_id
            ticket.save()

            comment = comment_form.save(False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            messages.success(request,"Your ticket has been logged", extra_tags='alert alert-success')

            return redirect(reverse('ticket-detail', args={ticket.pk}))
        else:
            print "TICKET FORM NOT VALID"
            print ticket_form

    else:
        ticket_form = TicketForm()
        # Set up the list of products so it only shows the active products for the user
        user_purchases = Purchase.objects.filter(user=request.user)
        active_purchases = Purchase.objects.filter(license_end__gte=timezone.now())
        purchases = user_purchases & active_purchases
        active_products = [purchase.product_id for purchase in purchases]
        ticket_form.fields['product'].queryset = Product.objects.filter(pk__in=active_products)

        comment_form = CommentForm(request.POST)

    args = {'ticket_form':ticket_form, 'comment_form':comment_form}
    args.update(csrf(request))

    return render(request, 'tickets/ticket_form.html',args)


@login_required()
def new_comment(request, ticket_id):
    # Add new comment to ticket
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            messages.success(request, "Your comment has been logged", extra_tags='alert alert-success')

            return redirect(reverse('ticket-detail', args={ticket.pk}))
    else:
        comment_form = CommentForm(request.POST)
        print "comment_form"
        print comment_form
        args = {
            'comment_form': comment_form,
            'form_action': reverse('new-comment', args=[ticket_id]),
            'button_text': 'Add Comment',
            'ticket_id': ticket_id
        }
        print "ARGS"
        print args
        args.update(csrf(request))

        return render(request, 'tickets/comment_form.html', args)


# Automatically check after new comment and update the ticket status depending on the user that commented
def update_pending_status(request, ticket):
    last_comment = ticket.comments.all().order_by('created_date').last()
    if last_comment.user.is_staff:
        print "IS STAF"
        ticket.status = "PCR"
    else:
        print "IS CUSTOMER"
        ticket.status = "PER"
    ticket.save()


def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.status="CLS"
    ticket.closed_date=timezone.now()
    ticket.save()
    messages.success(request, "The ticket has been closed", extra_tags='alert alert-success')
    return redirect(reverse('ticket-detail', args={ticket_id}))


def reopen_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    last_comment = ticket.comments.all().order_by('created_date').last()
    if last_comment.user.is_staff:
        ticket.status = "PCR"
    else:
        ticket.status = "PER"
    ticket.closed_date=None
    ticket.save()
    messages.success(request, "The ticket has been re-opened", extra_tags='alert alert-success')
    return redirect(reverse('ticket-detail', args={ticket_id}))


# NOT WORKING, 'form_action': reverse('edit-comment', args={'ticket_id': ticket.id, 'comment_id': comment.id}),
def edit_comment(request, ticket_id, comment_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    print "COMMENT"
    print comment

    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, "You have updated your comment!", extra_tags='alert alert-success')

            return redirect(reverse('ticket-detail', args={ticket_id}))
    else:

        comment_form = CommentForm(instance=comment)
        print comment_form
        print "Before args"
        print ticket_id
        print comment_id

        args = {
            'form': comment_form,
            'form_action': reverse('edit-comment', args=[ticket_id, comment_id]),
            'button_text': 'Update Comment',
            'ticket_id':ticket_id,
            'comment_id': comment_id

        }
        print "ARGSSSS"
        print args
        args.update(csrf(request))

        return render(request, 'tickets/comment_form.html', args)


def delete_comment(request, ticket_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    messages.success(request, "Your comment was deleted!", extra_tags='alert alert-success')

    return redirect(reverse('ticket-detail', args={ticket_id}))
