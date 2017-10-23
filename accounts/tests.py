from django.test import TestCase
from django.core.urlresolvers import reverse
from django import forms
from forms import UserRegistrationForm
from accounts.models import User
from products.models import Purchase, Product


class ProfilePageVisitorTest(TestCase):
    """ Test profile page for visitors (not logged in) users """

    def test_redirect_to_login_page_when_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/login/?next=/profile/')


class ProfilePageTest(TestCase):
    """ Test that the profile page renders correctly """

    def setUp(self):
        super(ProfilePageTest, self).setUp()
        self.user = User.objects.create_user(username='admin1@admin.com',
                                             email='admin1@admin.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test', is_staff='True')
        self.user.save()
        login = self.client.login(username='admin1@admin.com',
                                  password='letmein1')
        self.assertTrue(login)

    def test_profile_menu_item_has_class_active(self):
        profile_page = self.client.get('/profile/')
        self.assertIn('id="nav-profile" class="active"', profile_page.content)

    def test_check_template_is_correct(self):
        home_page = self.client.get('/profile/')
        self.assertTemplateUsed(home_page, "profile.html")

    def tearDown(self):
        self.user.delete()


class ProfilePageStaffUserTest(TestCase):
    """
    Test specific parts of the profile page that should load
    different content when a staff user is authenticated
    """

    def setUp(self):
        """ Create staff user for test and log it in"""
        super(ProfilePageStaffUserTest, self).setUp()
        self.user = User.objects.create_user(username='admin1@admin.com',
                                             email='admin1@admin.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test', is_staff='True')
        self.user.save()

        login = self.client.login(username='admin1@admin.com',
                                  password='letmein1')
        self.assertTrue(login)

    def test_check_user_type_message_is_staff_for_staff_user(self):
        """
        Test that the message below the personal details
        is correct for staff users
        """

        profile_page = self.client.get('/profile/')
        self.assertIn('<p id="staff-msg"', profile_page.content)

    def test_check_cta_is_shortcuts_for_staff_user(self):
        """
        Test that the call to action box on the right column
        is the correct one for staff users
        """

        profile_page = self.client.get('/profile/')
        self.assertIn('<div id="cta-shortcuts" class="cta">',
                      profile_page.content)

    def test_check_products_section_not_shown_for_staff_user(self):
        """
        Test that the products section is not showed for staff users as
        staff shouldn't buy products from
        """

        profile_page = self.client.get('/profile/')
        self.assertNotIn('<div id="products" ', profile_page.content)

    def tearDown(self):
        self.user.delete()


class ProfilePageActiveCustomerUserTest(TestCase):
    """
    Test specific parts of the profile page that should load
    different content when an active customer user
    (has at least 1 active license) is authenticated
    """

    def setUp(self):
        """ Create active user for test and log it in """
        super(ProfilePageActiveCustomerUserTest, self).setUp()
        self.user = User.objects.create_user(username='active@test.com',
                                             email='active@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test', is_staff='False')
        self.user.save()
        self.product = Product.objects.create(name="test")
        self.product.save()
        self.purchase = \
            Purchase.objects.create(user=self.user, product=self.product,
                                    license_end="2999-01-01T00:00:00Z")
        self.purchase.save()
        login = self.client.login(username='active@test.com',
                                  password='letmein1')
        self.assertTrue(login)

    def test_check_user_type_message_is_active_for_active_customer_user(self):
        """
        Test that the message below the personal details
        is correct for active users
        """

        profile_page = self.client.get('/profile/')
        self.assertIn('<p id="active-msg"', profile_page.content)

    def test_check_cta_is_contactus_for_active_customer_user(self):
        """
        Test that the call to action box on the right column
        is the correct one for active users
        """
        profile_page = self.client.get('/profile/')
        self.assertIn('<div id="cta-contactus" class="cta">',
                      profile_page.content)

    def test_check_products_section_is_shown_for_active_customer_user(self):
        """ Test that the products section is shown for active users """
        profile_page = self.client.get('/profile/')
        self.assertIn('<div id="products" ', profile_page.content)

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.purchase.delete()


class ProfilePageInactiveUserTest(TestCase):
    """
    Test specific parts of the profile page that should load different content
    when a registered user (doesn't have any active license) is authenticated
    """

    def setUp(self):
        super(ProfilePageInactiveUserTest, self).setUp()
        self.user = User.objects.create_user(username='inactive@test.com',
                                             email='inactive@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test', is_staff='False')
        self.user.save()
        login = self.client.login(username='inactive@test.com',
                                  password='letmein1')
        self.assertTrue(login)

    def test_check_user_type_message_is_inactive_for_inactive_user(self):
        """
        Test that the message below the personal details
        is correct for registered users
        """

        profile_page = self.client.get('/profile/')
        self.assertIn('<p id="inactive-msg"', profile_page.content)

    def test_check_cta_is_offer_for_inactive_user(self):
        """
        Test that the call to action box on the right column
        is the correct one for registered users
        """

        profile_page = self.client.get('/profile/')
        self.assertIn('<div id="cta-offer" class="cta">', profile_page.content)

    def test_check_products_section_is_shown_for_inactive_user(self):
        """ Test that the products section is shown for registered users """

        profile_page = self.client.get('/profile/')
        self.assertIn('<div id="products" ', profile_page.content)

    def tearDown(self):
        self.user.delete()


class RegistrationFormTest(TestCase):
    """
    Test that RegistrationForm validation works correctly
    with different password and email inputs
    """

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
        self.assertRaisesMessage(forms.ValidationError,
                                 "Please enter your password")

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
        self.assertRaisesMessage(forms.ValidationError,
                                 "Please confirm your password")

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
        self.assertRaisesMessage(forms.ValidationError,
                                 "Password must be at least 8 characters long")

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
        self.assertRaisesMessage(forms.ValidationError,
                                 "Password must contain at least 1 digit")

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
        self.assertRaisesMessage(forms.ValidationError,
                                 "Password must contain at least 1 letter")

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
        self.assertRaisesMessage(forms.ValidationError,
                                 "Passwords do not match")

    def test_form_fails_when_email_not_unique(self):

        self.user = User.objects.create(username='admin@admin.com',
                                        email='admin@admin.com',
                                        password='letmein1',
                                        first_name='test', last_name='test',
                                        company='test')
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
        self.assertRaisesMessage(forms.ValidationError,
                                 "That email address is already registered")
