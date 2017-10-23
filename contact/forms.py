from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Form to send a query.
    After filling out the form users will receive an email.
    """

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'query']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            message = "Please enter your email address"
            raise forms.ValidationError(message)

        return email
