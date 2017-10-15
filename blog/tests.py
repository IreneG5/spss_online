from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from blog.views import post_list


class BlogPageTest(TestCase):
    def test_blog_page_resolves(self):
        blog_page = resolve('/blog/')
        self.assertEqual(blog_page.func, post_list)

    def test_blog_page_status_code_is_ok(self):
        blog_page = self.client.get('/blog/')
        self.assertEqual(blog_page.status_code, 200)

    def test_check_content_is_correct(self):
        # Test fails because it dynamically change the active class in the navbar when the page loads (based on url)
        #  and the template doesn't' show it.
        # Removing the if statement in this line in base.py makes the test pass
        # <li {% if request.resolver_match.url_name == 'blog' or request.resolver_match.url_name == 'post-detail'%}
        #                class="active"{% endif %}>
        blog_page = self.client.get('/blog/')
        self.assertTemplateUsed(blog_page, "blog/blog_posts.html")
        blog_page_template_output = render_to_response("blog/blog_posts.html").content
        self.assertEqual(blog_page.content, blog_page_template_output)
