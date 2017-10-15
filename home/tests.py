from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from home.views import get_index


class HomePageTest(TestCase):
    """ Test home page """
    def test_home_page_resolves(self):
        home_page = resolve('/')
        self.assertEqual(home_page.func, get_index)

    def test_home_page_status_code_is_ok(self):
        home_page = self.client.get('/')
        self.assertEqual(home_page.status_code, 200)

    def test_check_content_is_correct(self):
        # Test fails because it dynamically change the active class in the navbar when the page loads (based on url)
        #  and the template doesn't' show it.
        home_page = self.client.get('/')
        self.assertTemplateUsed(home_page, "index.html")
        home_page_template_output = render_to_response("index.html").content
        self.assertEqual(home_page.content, home_page_template_output)
