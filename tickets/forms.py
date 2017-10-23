from django import forms
from .models import Ticket, Comment
from products.models import Purchase


class TicketForm(forms.ModelForm):
    """
    Form to create new tickets
    The field product only shows the products related to
    purchases whose license are active
    """

    product = forms.ModelChoiceField(queryset=Purchase.objects.all())

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ['subject', 'reason', 'product']


class CommentForm(forms.ModelForm):
    """ Form to create new comments """

    class Meta:
        model = Comment
        fields = ['comment']
