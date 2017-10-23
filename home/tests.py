from django.test import TestCase
from accounts.models import User


class HomePageTest(TestCase):
    """ Test home page """

    def test_index_menu_item_has_class_active(self):
        home_page = self.client.get('/')
        self.assertIn('id="nav-home" class="active"', home_page.content)


class MenuVisitorUserTest(TestCase):
    """ Test menu nav bar """

    def test_menu_shows_login_and_register_for_not_logged_users(self):
        home_page = self.client.get('/')
        self.assertIn('id="nav-register"', home_page.content)
        self.assertIn('id="nav-login"', home_page.content)

    def test_menu_doesnt_show_profile_tickets_log_for_not_logged_users(self):
        home_page = self.client.get('/')
        self.assertNotIn('id="nav-profile"', home_page.content)
        self.assertNotIn('id="nav-tickets"', home_page.content)
        self.assertNotIn('id="nav-logout"', home_page.content)


class MenuLoggedUserTest(TestCase):
    """
    Test that correct menu items are shown when user
    """

    def setUp(self):
        super(MenuLoggedUserTest, self).setUp()
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

    def test_menu_doesnt_show_register_and_login_for_logged_users(self):
        home_page = self.client.get('/')
        self.assertNotIn('id="nav-register"', home_page.content)
        self.assertNotIn('id="nav-login"', home_page.content)

    def test_menu_shows_profile_tickets_and_logout_for_logged_users(self):
        home_page = self.client.get('/')
        self.assertIn('id="nav-profile"', home_page.content)
        self.assertIn('id="nav-tickets"', home_page.content)
        self.assertIn('id="nav-logout"', home_page.content)

    def tearDown(self):
        self.user.delete()
