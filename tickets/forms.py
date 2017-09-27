from django import forms
from .models import Ticket, Comment
from products.models import Purchase, Product


class TicketForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Purchase.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TicketForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ['subject', 'reason','product']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


