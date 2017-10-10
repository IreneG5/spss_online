from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User



class UserRegistrationForm(UserCreationForm):

    # Extra fields not included in the User Model
    company = forms.CharField(max_length=100, label='Company')

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'company']
        exclude = ['username']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            message = "Please enter your password"
            raise forms.ValidationError(message)

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            message = "Please confirm your password"
            raise forms.ValidationError(message)

        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise forms.ValidationError(message)

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            message = "Please enter your email address"
            raise forms.ValidationError(message)

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            message = "Please enter your first name"
            raise forms.ValidationError(message)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            message = "Please enter your last name"
            raise forms.ValidationError(message)
        return last_name

    def clean_company(self):
        company = self.cleaned_data.get('company')
        if not company:
            message = "Please enter your company name"
            raise forms.ValidationError(message)
        return company

    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)

        # automatically set to email address to create a unique identifier
        instance.username = instance.email

        if commit:
            instance.save()

        return instance

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.Form):
    email_address = forms.EmailField(widget = forms.TextInput(attrs = {'class':'required'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_email_address(self):
        email = self.cleaned_data.get('email_address')
        if self.user and self.user.email == email:
            return email
        if User.objects.filter(email=email).count():
            raise forms.ValidationError(u'That email address already exists.')
        return email