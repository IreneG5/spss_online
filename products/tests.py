from django.test import TestCase


class ProductsPageTest(TestCase):
    """ Test products page """

    def test_products_menu_item_has_class_active(self):
        products_page = self.client.get('/products/')
        self.assertIn('id="nav-products" class="active"',
                      products_page.content)
