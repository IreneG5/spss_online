from django.test import TestCase
from django.shortcuts import render_to_response
from django.utils import timezone
from django import forms
from forms import UserRegistrationForm

from accounts.models import User


class ProfilePageTest(TestCase):
    """ Test profile page renders correctly for authenticated user """
    def setUp(self):

        super(ProfilePageTest, self).setUp()
        self.user = User.objects.create(username='admin1@admin.com', email='admin1@admin.com', password='letmein1',
                                        first_name='test', last_name='test', company='test', is_staff=1, is_active=1,
                                        is_superuser=1, date_joined=timezone.now())
        self.user.save()
        self.login = self.client.login(username='admin1@admin.com', password='letmein1')
        self.assertEqual(self.login, True)

    def test_check_content_is_correct(self):
        home_page = self.client.get('/profile/')
        self.assertTemplateUsed(home_page, "profile.html")
        home_page_template_output = render_to_response("profile.html", {'user': self.user}).content
        self.assertEqual(home_page.content, home_page_template_output)


class RegistrationFormTest(TestCase):
    """ Test RegistrationForm validation with different password and email situations """

    def test_form_is_valid(self):
        form = UserRegistrationForm({
            'username': 'test@test.com',
            'email': 'test@test.com',
            'password1': 'letmein1',
            'password2': 'letmein1',
            'first_name': 'test',
            'last_name': 'test',
            'company': 'test'
        })
        self.assertTrue(form.is_valid())

    def test_form_fails_when_missing_password1(self):
        form = UserRegistrationForm({
            'username': 'test@test.com',
            'email': 'test@test.com',
            'password2': 'letmein1',
            'first_name': 'test',
            'last_name': 'test',
            'company': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Please enter your password")

    def test_form_fails_when_missing_password2(self):
        form = UserRegistrationForm({
            'username': 'test@test.com',
            'email': 'test@test.com',
            'password1': 'letmein1',
            'first_name': 'test',
            'last_name': 'test',
            'company': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Please confirm your password")

    def test_form_fails_when_password_too_short(self):
        form = UserRegistrationForm({
            'username': 'test@test.com',
            'email': 'test@test.com',
            'password1': 'letme',
            'password2': 'letme',
            'first_name': 'test',
            'last_name': 'test',
            'company': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Password must be at least 8 characters long")

    def test_form_fails_when_password_not_numbers(self):
        form = UserRegistrationForm({
            'username': 'test@test.com',
            'email': 'test@test.com',
            'password1': 'letmeinn',
            'password2': 'letmeinn',
            'first_name': 'test',
            'last_name': 'test',
            'company': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Password must contain at least 1 digit")

    def test_form_fails_when_password_not_letters(self):
        form = UserRegistrationForm({
            'username': 'test@test.com',
            'email': 'test@test.com',
            'password1': '12345678',
            'password2': '12345678',
            'first_name': 'test',
            'last_name': 'test',
            'company': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Password must contain at least 1 letter")

    def test_form_fails_when_password_dont_match(self):
        form = UserRegistrationForm({
            'username': 'test@test.com',
            'email': 'test@test.com',
            'password1': 'letmein1',
            'password2': 'letmein2',
            'first_name': 'test',
            'last_name': 'test',
            'company': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Passwords do not match")

    def test_form_fails_when_email_not_unique(self):

        self.user = User.objects.create(username='admin@admin.com', email='admin@admin.com', password='letmein1',
                                        first_name='test', last_name='test', company='test')
        self.user.save()

        form = UserRegistrationForm({
            'username': 'admin@admin.com',
            'email': 'admin@admin.com',
            'password1': 'letmein1',
            'password2': 'letmein1',
            'first_name': 'test',
            'last_name': 'test',
            'company': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "That email address is already registered")
