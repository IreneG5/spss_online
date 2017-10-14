# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.context_processors import csrf
from .forms import ContactForm


# Create your views here.
def get_contact(request):
    """
    Return the contact page with form. Save the form when it is valid and return a message.
    Use Google Maps Embed API to show the map
    """
    
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save()
            messages.success(request, "Your query has been sent. We will get in touch shortly",
                             extra_tags='alert alert-success')
            send_email(request, contact)
            send_email_notification(request, contact)

            return redirect(reverse('contact'))

    else:
        user = request.user
        # if user is logged in, pre-populate fields in form
        if user.is_authenticated:
            contact_form = ContactForm(initial={'first_name': user.first_name, 'last_name': user.last_name,
                                                'email': user.email})
        else:
            contact_form = ContactForm()

    args = {'form': contact_form}
    args.update(csrf(request))
    return render(request, 'contact.html', args)


def send_email(request, contact):
    """ Send an email to the email address in the contact us form"""

    subject = "Thank you for your query."
    message = "Hi %s,\n\n" \
              "Thank you for your query.\n\n" \
              "A member of our team will contact you shortly.\n\n" \
              "In the meantime, why don't you have a look at our blog: " \
              "https://spss-online.herokuapp.com/blog/\n\n" \
              "Kind regards\n easySPSS Team" % contact.first_name

    from_email = "easyspssweb@gmail.com"
    send_mail(subject, message, from_email, [contact.email])


def send_email_notification(request, contact):
    """ Send a notification email to the company's email address indicating they have received a new query """

    subject = "You have a new query."
    message = "Hi,\n\n" \
              "%s %s sent you the query below.\n\n" \
              "Please get in touch shortly.\n\n" \
              "Email address: %s\n"\
              "Query:\n %s\n\n\n"\
              "Kind regards,\n easySPSS Team" % (contact.first_name, contact.last_name, contact.email, contact.query)

    from_email = "easyspssweb@gmail.com"
    send_mail(subject, message, from_email, ['easyspssweb@gmail.com'])
