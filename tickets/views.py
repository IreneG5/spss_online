# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from .forms import TicketForm, CommentForm
from tickets.models import Comment, Ticket
from products.models import Purchase, Product


# Create your views here.
@login_required()
def tickets(request):
    # Get list of tickets for the logged user
    print request.user.id
    print Ticket.objects.filter(user_id=request.user.id)
    args = {'tickets': Ticket.objects.filter(user_id=request.user.id),
            'comments': Comment.objects.filter(user_id=request.user.id).order_by('-created_date')}
    return render(request, 'tickets/tickets.html', args)


@login_required()
def ticket_detail(request, ticket_id):
    # Get details of specific ticket with comments
    ticket_ = get_object_or_404(Ticket, pk=ticket_id)
    comments = Comment.objects.filter(ticket_id=ticket_id)
    args = {'ticket':ticket_, 'comments':comments}
    args.update(csrf(request))
    return render(request, 'tickets/ticketdetail.html', args)


@login_required()
def new_ticket(request):
    # Create new ticket
    if request.method=='POST':
        ticket_form = TicketForm(request.POST)
        comment_form = CommentForm(request.POST)

        if ticket_form.is_valid() and comment_form.is_valid():
            ticket = ticket_form.save(False)
            ticket.user = request.user
            ticket.save()

            comment = comment_form.save(False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            messages.success(request,"Your ticket has been logged", extra_tags='alert alert-success')

            return redirect(reverse('ticket-detail', args={ticket.pk}))
    else:
        ticket_form = TicketForm()
        comment_form = CommentForm(request.POST)

    args={'ticket_form':ticket_form,
          'comment_form':comment_form}
    args.update(csrf(request))

    return render(request, 'tickets/ticket_form.html',args)


@login_required()
def new_comment(request, ticket_id):
    # Add new comment to ticket
    print "NEW COMMENT #####################"
    ticket= get_object_or_404(Ticket, pk=ticket_id)
    print ticket
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            messages.success(request, "Your comment has been logged", extra_tags='alert alert-success')
            update_pending_status(request, ticket)
            print "STATUS:"
            print ticket.status


            return redirect(reverse('ticket-detail', args={ticket.pk}))
    else:
        comment_form = CommentForm(request.POST)
        print "ELSE new_cooment"
        print comment_form
        args = {
            'comment_form': comment_form,
            'form_action': reverse('new-comment', args={ticket.id}),
            'button_text': 'Add Comment',
            'ticket_id': ticket_id
        }

        args.update(csrf(request))
        print args
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
    ticket.save()
    return redirect(reverse('ticket-detail', args={ticket_id}))


def reopen_ticket(request, ticket_id):
    print "REOPEEEEEEEEEEEEEEN"
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    last_comment = ticket.comments.all().order_by('created_date').last()
    if last_comment.user.is_staff:
        ticket.status = "PCR"
    else:
        ticket.status = "PER"
    ticket.save()
    return redirect(reverse('ticket-detail', args={ticket_id}))

