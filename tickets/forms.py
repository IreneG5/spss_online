from django import forms
from .models import Ticket, Comment
from products.models import Purchase


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'reason', 'product']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
