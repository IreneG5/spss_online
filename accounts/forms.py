from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Render form to allow registration.
    All fields are required.
    Additional validation for password: not empty, confirmation match and password strength
    Additional validation for email: unique email
    """

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
        # Validate password1 not empty and strength
        password1 = self.cleaned_data.get('password1')
        if not password1:
            message = "Please enter your password"
            raise forms.ValidationError(message)

        min_length = 8

        # check for length
        if len(password1) < min_length:
            message = "Password must be at least 8 characters long"
            raise forms.ValidationError(message)

        # check for digit
        if not any(char.isdigit() for char in password1):
            message = "Password must contain at least 1 digit"
            raise forms.ValidationError(message)

        # check for letter
        if not any(char.isalpha() for char in password1):
            message = "Password must contain at least 1 letter"
            raise forms.ValidationError(message)

        return password1

    def clean_password2(self):
        # Validate password 2 not empty and matches password1
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
        # Validate email not empty and unique
        email = self.cleaned_data.get('email')

        if not email:
            message = "Please enter your email address"
            raise forms.ValidationError(message)
        else:
            users = User.objects.all()
            for user in users:
                if user.email == email:
                    message = "That email address is already registered"
                    raise forms.ValidationError(message)

        return email

    def clean_first_name(self):
        # Validate firs_name not empty
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            message = "Please enter your first name"
            raise forms.ValidationError(message)
        return first_name

    def clean_last_name(self):
        # Validate last_name not empty
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            message = "Please enter your last name"
            raise forms.ValidationError(message)
        return last_name

    def clean_company(self):
        # Validate company not empty
        company = self.cleaned_data.get('company')
        if not company:
            message = "Please enter your company name"
            raise forms.ValidationError(message)
        return company

    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)
        instance.username = instance.email

        if commit:
            instance.save()

        return instance

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class UserLoginForm(forms.Form):
    """ Form to authenticate user using email and password """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
