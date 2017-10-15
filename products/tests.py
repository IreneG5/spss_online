from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from products.views import all_products


class ProductsPageTest(TestCase):
    def test_product_page_resolves(self):
        products_page = resolve('/products/')
        self.assertEqual(products_page.func, all_products)

    def test_product_page_status_code_is_ok(self):
        products_page = self.client.get('/products/')
        self.assertEqual(products_page.status_code, 200)

    def test_check_content_is_correct(self):
        # Test fails because it dynamically change the active class in the navbar when the page loads (based on url)
        #  and the template doesn't' show it.
        products_page = self.client.get('/products/')
        self.assertTemplateUsed(products_page, "products/products.html")
        products_page_template_output = render_to_response("products/products.html").content
        self.assertEqual(products_page.content, products_page_template_output)
