# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from accounts.models import User
from products.models import Product, Purchase
from tickets.models import Ticket, Comment


class TicketsPageVisitorTest(TestCase):
    """ Test tickets page for visitors (not logged in) users """

    def test_redirect_to_login_page_when_not_logged_in(self):
        response = self.client.get(reverse('tickets-list'))
        self.assertRedirects(response, '/login/?next=/tickets/')


class TicketsPageTest(TestCase):
    """ Test Tickets Page general functionality """

    def setUp(self):
        super(TicketsPageTest, self).setUp()
        self.user = User.objects.create_user(username='staff@test.com',
                                             email='staff@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test',
                                             is_staff='True')
        self.user.save()
        self.client.login(username='staff@test.com',
                          password='letmein1')

    def test_tickets_menu_item_has_class_active(self):
        tickets_page = self.client.get('/tickets/')
        self.assertIn('id="nav-tickets" class="active"',
                      tickets_page.content)

    def tearDown(self):
        self.user.delete()


class TicketDetailPageTest(TestCase):
    """ Test Ticket Detail Page general functionality """

    def setUp(self):
        super(TicketDetailPageTest, self).setUp()
        self.user_staff = User.objects.create_user(username='staff@test.com',
                                                   email='staff@test.com',
                                                   password='letmein1',
                                                   first_name='test',
                                                   last_name='test',
                                                   company='test',
                                                   is_staff='True')
        self.user_staff.save()
        self.client.login(username='staff@test.com',
                          password='letmein1')

        self.user_active = User.objects.create_user(username='active@test.com',
                                                    email='active@test.com',
                                                    password='letmein1',
                                                    first_name='customer',
                                                    last_name='test',
                                                    company='test',
                                                    is_staff='False')
        self.user_active.save()

        self.product = Product.objects.create(name="test")
        self.product.save()

        self.ticket = Ticket.objects.create(subject='test',
                                            user=self.user_active,
                                            product=self.product)
        self.ticket.save()
        self.comment_active = Comment.objects.create(user=self.user_active,
                                                     ticket=self.ticket,
                                                     comment='test')
        self.comment_active.save()

    def test_tickets_menu_item_has_class_active(self):
        ticket_detail = self.client.get('/tickets/1/')
        self.assertIn('id="nav-tickets" class="active"',
                      ticket_detail.content)

    def tearDown(self):
        self.user_staff.delete()
        self.user_active.delete()
        self.product.delete()
        self.comment_active.delete()
        self.ticket.delete()


class TicketsPageInactiveUserTest(TestCase):
    """ Test tickets page for logged users that are not active customers """
    def setUp(self):
        super(TicketsPageInactiveUserTest, self).setUp()
        self.user = User.objects.create_user(username='inactive@test.com',
                                             email='inactive@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test',
                                             is_staff='False')
        self.user.save()
        self.client.login(username='inactive@test.com',
                          password='letmein1')
        self.product = Product.objects.create(name="test")
        self.product.save()

    def test_message_shown_for_inactive_user(self):
        """
        Test that a message is shown for inactive users indicating
        they are not allowed to open/edit tickets
        """

        tickets_page = self.client.get('/tickets/')
        self.assertIn('id="tickets-inactive-msg"', tickets_page.content)

    def test_open_ticket_button_not_shown_for_inactive_user(self):
        tickets_page = self.client.get('/tickets/')
        self.assertNotIn('id="open-ticket"', tickets_page.content)

    def tearDown(self):
        self.user.delete()


class TicketsPageActiveCustomerUserTest(TestCase):
    """ Test tickets page for active customer users """

    def setUp(self):
        super(TicketsPageActiveCustomerUserTest, self).setUp()
        self.user = User.objects.create_user(username='active@test.com',
                                             email='active@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test',
                                             is_staff='False')
        self.user.save()
        self.client.login(username='active@test.com',
                          password='letmein1')
        self.product = Product.objects.create(name="test")
        self.product.save()
        self.purchase = \
            Purchase.objects.create(user=self.user, product=self.product,
                                    license_end="2999-01-01T00:00:00Z")
        self.purchase.save()

    def test_message_not_shown_for_active_user(self):
        tickets_page = self.client.get('/tickets/')
        self.assertNotIn('id="tickets-inactive-msg"',
                         tickets_page.content)

    def test_open_ticket_button_shown_for_active_user(self):
        tickets_page = self.client.get('/tickets/')
        self.assertIn('id="open-ticket"', tickets_page.content)

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.purchase.delete()


class TicketsPageStaffUserTest(TestCase):
    """ Test tickets page for staff users """

    def setUp(self):
        super(TicketsPageStaffUserTest, self).setUp()
        self.user_staff = User.objects.create_user(username='staff@test.com',
                                                   email='staff@test.com',
                                                   password='letmein1',
                                                   first_name='test',
                                                   last_name='test',
                                                   company='test',
                                                   is_staff='True')
        self.user_staff.save()
        self.client.login(username='staff@test.com',
                          password='letmein1')

    def test_message_not_shown_for_staff_user(self):
        tickets_page = self.client.get('/tickets/')
        self.assertNotIn('id="tickets-inactive-msg"', tickets_page.content)

    def test_open_ticket_button_not_shown_for_staff_user(self):
        tickets_page = self.client.get('/tickets/')
        self.assertNotIn('id="open-ticket"', tickets_page.content)

    def tearDown(self):
        self.user_staff.delete()


class TicketsPageStatusNewTest(TestCase):
    """
    Test that tickets are created with status New (staff view)
    For this test is needed a staff user to login, a customer user
    (with an active license) to create a ticket, a ticket and a comment
    """

    def setUp(self):
        super(TicketsPageStatusNewTest, self).setUp()
        self.user_staff = User.objects.create_user(username='staff@test.com',
                                                   email='staff@test.com',
                                                   password='letmein1',
                                                   first_name='test',
                                                   last_name='test',
                                                   company='test',
                                                   is_staff='True')
        self.user_staff.save()
        self.client.login(username='staff@test.com',
                          password='letmein1')

        self.user_active = User.objects.create_user(username='active@test.com',
                                                    email='active@test.com',
                                                    password='letmein1',
                                                    first_name='customer',
                                                    last_name='test',
                                                    company='test',
                                                    is_staff='False')
        self.user_active.save()

        self.product = Product.objects.create(name="test")
        self.product.save()
        self.purchase = \
            Purchase.objects.create(user=self.user_active,
                                    product=self.product,
                                    license_end="2999-01-01T00:00:00Z")
        self.purchase.save()
        self.ticket = Ticket.objects.create(subject='test',
                                            user=self.user_active,
                                            product=self.product)
        self.ticket.save()
        self.comment_active = Comment.objects.create(user=self.user_active,
                                                     ticket=self.ticket,
                                                     comment='test')
        self.comment_active.save()

    def test_ticket_status_new_for_new_ticket(self):
        tickets_page = self.client.get('/tickets/')
        self.assertIn('<td id="status-1">NEW', tickets_page.content)

    def tearDown(self):
        self.user_staff.delete()
        self.user_active.delete()
        self.product.delete()
        self.purchase.delete()
        self.comment_active.delete()
        self.ticket.delete()


class TicketsPageStatusPCRTest(TestCase):
    """
    Test that the ticket status changes to PCR
    (Pending Customer Response) (staff view)
    when the last comment was added by a staff user
    For this test is needed a staff user to login, a customer user
    (with an active license) to create a ticket, a ticket
    and two comments, first one added by
    the customer and last one added by a staff user.
    """

    def setUp(self):
        super(TicketsPageStatusPCRTest, self).setUp()
        self.user_staff = User.objects.create_user(username='staff@test.com',
                                                   email='staff@test.com',
                                                   password='letmein1',
                                                   first_name='test',
                                                   last_name='test',
                                                   company='test',
                                                   is_staff='True')
        self.user_staff.save()
        self.client.login(username='staff@test.com',
                          password='letmein1')

        self.user_active = User.objects.create_user(username='active@test.com',
                                                    email='active@test.com',
                                                    password='letmein1',
                                                    first_name='customer',
                                                    last_name='test',
                                                    company='test',
                                                    is_staff='False')
        self.user_active.save()

        self.product = Product.objects.create(name="test")
        self.product.save()
        self.purchase = \
            Purchase.objects.create(user=self.user_active,
                                    product=self.product,
                                    license_end="2999-01-01T00:00:00Z")
        self.purchase.save()
        self.ticket = Ticket.objects.create(subject='test',
                                            user=self.user_active,
                                            product=self.product)
        self.ticket.save()
        self.comment_active = Comment.objects\
            .create(user=self.user_active, ticket=self.ticket,
                    comment='test-active',
                    created_date="2017-10-01T00:00Z")
        self.comment_active.save()
        self.comment_staff = Comment.objects\
            .create(user=self.user_staff, ticket=self.ticket,
                    comment='test-staff',
                    created_date="2017-10-02T00:00Z")
        self.comment_staff.save()

    def test_ticket_status_PCR_when_last_comment_by_staff(self):
        tickets_page = self.client.get('/tickets/')
        self.assertIn('<td id="status-1">PCR', tickets_page.content)

    def tearDown(self):
        self.user_staff.delete()
        self.user_active.delete()
        self.product.delete()
        self.purchase.delete()
        self.comment_active.delete()
        self.comment_staff.delete()
        self.ticket.delete()


class TicketsPageStatusPERTest(TestCase):
    """
    Test that the ticket status changes to PER
    (Pending easySPSS Response) (staff view)
    when the last comment was added by a customer.
    For this test is needed a staff user to login, a customer user
    (with an active license) to create a ticket, a ticket
    and two comments, first one added by
    the customer when opening the ticket and last one
    added also by the customer.
    """

    def setUp(self):
        super(TicketsPageStatusPERTest, self).setUp()
        self.user_staff = User.objects.create_user(username='staff@test.com',
                                                   email='staff@test.com',
                                                   password='letmein1',
                                                   first_name='test',
                                                   last_name='test',
                                                   company='test',
                                                   is_staff='True')
        self.user_staff.save()
        self.client.login(username='staff@test.com',
                          password='letmein1')

        self.user_active = User.objects.create_user(username='active@test.com',
                                                    email='active@test.com',
                                                    password='letmein1',
                                                    first_name='customer',
                                                    last_name='test',
                                                    company='test',
                                                    is_staff='False')
        self.user_active.save()

        self.product = Product.objects.create(name="test")
        self.product.save()
        self.purchase = \
            Purchase.objects.create(user=self.user_active,
                                    product=self.product,
                                    license_end="2999-01-01T00:00:00Z")
        self.purchase.save()
        self.ticket = Ticket.objects.create(subject='test',
                                            user=self.user_active,
                                            product=self.product)
        self.ticket.save()
        self.comment_active = Comment.objects\
            .create(user=self.user_active, ticket=self.ticket,
                    comment='test-active',
                    created_date="2017-10-01T00:00Z")
        self.comment_active.save()

        self.comment_active2 = Comment.objects\
            .create(user=self.user_active, ticket=self.ticket,
                    comment='test-active',
                    created_date="2017-10-02T00:00Z")
        self.comment_active2.save()

    def test_ticket_status_PER_when_last_comment_by_customer(self):
        tickets_page = self.client.get('/tickets/')
        self.assertIn('<td id="status-1">PER', tickets_page.content)

    def tearDown(self):
        self.user_staff.delete()
        self.user_active.delete()
        self.product.delete()
        self.purchase.delete()
        self.comment_active.delete()
        self.comment_active2.delete()
        self.ticket.delete()


class TicketDetailPageDeleteCommentsTest(TestCase):
    """ Test Tickets Detail Page delete comments """

    def setUp(self):
        super(TicketDetailPageDeleteCommentsTest, self).setUp()
        self.user_staff = User.objects.create_user(username='staff@test.com',
                                                   email='staff@test.com',
                                                   password='letmein1',
                                                   first_name='test',
                                                   last_name='test',
                                                   company='test',
                                                   is_staff='True')
        self.user_staff.save()
        self.client.login(username='staff@test.com',
                          password='letmein1')

        self.user_active = User.objects.create_user(username='active@test.com',
                                                    email='active@test.com',
                                                    password='letmein1',
                                                    first_name='customer',
                                                    last_name='test',
                                                    company='test',
                                                    is_staff='False')
        self.user_active.save()

        self.product = Product.objects.create(name="test")
        self.product.save()
        self.purchase = \
            Purchase.objects.create(user=self.user_active,
                                    product=self.product,
                                    license_end="2999-01-01T00:00:00Z")
        self.purchase.save()
        self.ticket = Ticket.objects.create(subject='test',
                                            user=self.user_active,
                                            product=self.product)
        self.ticket.save()
        self.comment_active = Comment.objects\
            .create(user=self.user_active, ticket=self.ticket,
                    comment='test-active',
                    created_date="2017-10-01T00:00Z")
        self.comment_active.save()
        self.comment_staff = Comment.objects\
            .create(user=self.user_staff, ticket=self.ticket,
                    comment='test-staff',
                    created_date="2017-10-02T00:00Z")
        self.comment_staff.save()

    def test_staff_can_delete_comments_if_more_than_one(self):
        tickets_page = self.client.get('/tickets/1/')
        self.assertIn('id="ticket-delete-comment" ', tickets_page.content)

    def tearDown(self):
        self.user_staff.delete()
        self.user_active.delete()
        self.product.delete()
        self.purchase.delete()
        self.comment_active.delete()
        self.comment_staff.delete()
        self.ticket.delete()


class TicketDetailPageCantDeleteCommentsTest(TestCase):
    """ Test Tickets Detail Page can't delete comments """

    def setUp(self):
        super(TicketDetailPageCantDeleteCommentsTest, self).setUp()
        self.user_staff = User.objects.create_user(username='staff@test.com',
                                                   email='staff@test.com',
                                                   password='letmein1',
                                                   first_name='test',
                                                   last_name='test',
                                                   company='test',
                                                   is_staff='True')
        self.user_staff.save()
        self.client.login(username='staff@test.com',
                          password='letmein1')

        self.user_active = User.objects.create_user(username='active@test.com',
                                                    email='active@test.com',
                                                    password='letmein1',
                                                    first_name='customer',
                                                    last_name='test',
                                                    company='test',
                                                    is_staff='False')
        self.user_active.save()

        self.product = Product.objects.create(name="test")
        self.product.save()
        self.purchase = \
            Purchase.objects.create(user=self.user_active,
                                    product=self.product,
                                    license_end="2999-01-01T00:00:00Z")
        self.purchase.save()
        self.ticket = Ticket.objects.create(subject='test',
                                            user=self.user_active,
                                            product=self.product)
        self.ticket.save()
        self.comment_active = Comment.objects.create(user=self.user_active,
                                                     ticket=self.ticket,
                                                     comment='test-active',
                                                     created_date="2017-10-01T00:00Z")
        self.comment_active.save()

    def test_staff_cant_delete_comments_if_less_than_two(self):
        tickets_page = self.client.get('/tickets/1/')
        self.assertNotIn('id="ticket-delete-comment" ', tickets_page.content)

    def tearDown(self):
        self.user_staff.delete()
        self.user_active.delete()
        self.product.delete()
        self.purchase.delete()
        self.comment_active.delete()
        self.ticket.delete()


class TicketDetailPageInactiveUserTest(TestCase):
    """ Test tickets page for logged users that are not active customers """

    def setUp(self):
        super(TicketDetailPageInactiveUserTest, self).setUp()
        self.user = User.objects.create_user(username='inactive@test.com',
                                             email='inactive@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test',
                                             is_staff='False')
        self.user.save()
        self.client.login(username='inactive@test.com',
                          password='letmein1')
        self.product = Product.objects.create(name="test")
        self.product.save()

        self.ticket = Ticket.objects.create(subject='test', user=self.user,
                                            product=self.product)
        self.ticket.save()
        self.comment = Comment.objects.create(user=self.user,
                                              ticket=self.ticket,
                                              comment='test')
        self.comment.save()

    def test_message_shown_for_inactive_user(self):
        """
        Test that a message is shown for inactive users indicating
        they are not allowed to open/edit tickets
        """

        tickets_page = self.client.get('/tickets/1/')
        self.assertIn('id="ticket-inactive-msg"', tickets_page.content)

    def test_buttons_not_shown_for_inactive_user(self):
        tickets_page = self.client.get('/tickets/1/')
        self.assertNotIn('id="open-ticket"', tickets_page.content)
        self.assertNotIn('id="ticket-close-ticket"', tickets_page.content)
        self.assertNotIn('id="ticket-add-comment"', tickets_page.content)

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.ticket.delete()
        self.comment.delete()


class TicketDetailPageClosedTicketTest(TestCase):
    """ Test tickets page when a ticket is closed """

    def setUp(self):
        super(TicketDetailPageClosedTicketTest, self).setUp()
        self.user = User.objects.create_user(username='active@test.com',
                                             email='active@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test',
                                             is_staff='False')
        self.user.save()
        self.client.login(username='active@test.com',
                          password='letmein1')
        self.product = Product.objects.create(name="test")
        self.product.save()
        self.purchase = \
            Purchase.objects.create(user=self.user, product=self.product,
                                    license_end="2999-01-01T00:00Z")
        self.purchase.save()

        self.ticket = Ticket.objects.create(subject='test',
                                            user=self.user,
                                            product=self.product,
                                            status='CLS',
                                            closed_date="2017-10-01T00:00Z")
        self.ticket.save()
        self.comment = Comment.objects.create(user=self.user,
                                              ticket=self.ticket,
                                              comment='test')
        self.comment.save()

    def test_buttons_not_shown_for_closed_ticket(self):
        tickets_page = self.client.get('/tickets/1/')
        self.assertNotIn('id="open-ticket"', tickets_page.content)
        self.assertNotIn('id="ticket-close-ticket"', tickets_page.content)
        self.assertNotIn('id="ticket-add-comment"', tickets_page.content)

    def test_reopen_buttons_shown_for_closed_ticket(self):
        tickets_page = self.client.get('/tickets/1/')
        self.assertIn('id="ticket-reopen-ticket"', tickets_page.content)

    def test_close_date_shown_for_closed_ticket(self):
        tickets_page = self.client.get('/tickets/1/')
        self.assertIn('Closed date:', tickets_page.content)

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.purchase.delete()
        self.ticket.delete()
        self.comment.delete()
