# -*- coding: utf-8 -*-
import arrow
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.core.mail import send_mail
from django import template
from accounts.forms import UserRegistrationForm, UserLoginForm
from products.models import Purchase
from tickets.models import Ticket


register = template.Library()


def register(request):
    """
    Render register.html template with RegistrationForm and process form if valid
    Send an welcome email to the user when the registration is successful
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))
            if user:
                send_email(request, user)
                messages.info(request, "Thanks for registering. You are now logged in.",
                              extra_tags='alert alert-success')
                auth.login(request, user)
                return redirect(reverse('profile'))
            else:
                messages.error(request, "Unable to log in. Please contact us", extra_tags='alert alert-danger')
    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'register.html', args)


@login_required(login_url='/login/')
def profile(request):
    """
    Render profile.html template.
    Some sections are different depending on the role of the user (registered, customer, staff)
    Use Purchases and Tickets models to show user its products and tickets
    """
    user = request.user
    if user.is_staff:
        # Get list of all tickets for staff user
        tickets = Ticket.objects.all().order_by('-opened_date')
        args = {'tickets': tickets}
    else:
        if user.is_customer:
            today = arrow.now()  # passed as argument to compare the products with an active licence in the template
            expire_soon = arrow.now().replace(
                days=+30).datetime  # passed as argument to highlight the products close to expire
            purchases = Purchase.objects.filter(user_id=request.user.id).order_by('license_end')
            tickets = Ticket.objects.filter(user_id=request.user.id).order_by('-opened_date')
            args = {'purchases': purchases, 'today': today, 'expire_soon': expire_soon, 'tickets': tickets}
        else:
            args = {}
    return render(request, "profile.html", args)


def login(request):
    """ Render profile.html template with UserLoginForm. If form is valid, log the user in """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have successfully logged in", extra_tags='alert alert-success')
                return redirect(reverse('profile'))
            else:
                form.add_error(None, "Your email or password was not recognised")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)


def logout(request):
    """ Log the authenticated user out """
    auth.logout(request)
    messages.success(request, 'You have successfully logged out', extra_tags='alert alert-success')
    return redirect(reverse('index'))


def send_email(request, contact):
    """ Send an welcome email to the user """

    subject = "Thank you for registering and Welcome to easySPSS."
    message = "Hi %s,\n\n" \
              "Welcome to easySPSS!\n\n" \
              "You can now visit your easySPSS at your convenience on http://spss-online.herokuapp.com\n\n" \
              "In easySPSS you will be able to:\n" \
              "- Buy SPSS Products online\n"\
              "- See all your purchases in one place\n"\
              "- Open support tickets if you need technical help\n"\
              "- Visit, comment and vote in our blog\n"\
              "- Avail the latest offers and discounts\n"\
              "- And much more...\n\n\n"\
              "Looking forward to see you around\n\n" \
              "Kind regards\n easySPSS Team" % contact.first_name

    from_email = "easyspssweb@gmail.com"
    send_mail(subject, message, from_email, [contact.email])
