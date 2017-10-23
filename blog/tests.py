from django.test import TestCase
from blog.models import Post, Category
from accounts.models import User


class BlogPageTest(TestCase):
    """ Test blog page """

    def test_blog_menu_item_has_class_active(self):
        blog_page = self.client.get('/blog/')
        self.assertIn('id="nav-blog" class="active"', blog_page.content)


class PostDetailPageTest(TestCase):
    """ Test post detail page """

    def setUp(self):
        super(PostDetailPageTest, self).setUp()
        self.user = User.objects.create_user(username='test@test.com',
                                             email='test@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test', is_staff='True')
        self.user.save()
        self.login = self.client.login(username='test@test.com',
                                       password='letmein1')
        self.assertTrue(self.login)
        self.post_category = Category.objects.create(name='test')
        self.post_category.save()
        self.post = Post.objects.create(author=self.user, title='Test',
                                        content='Test',
                                        created_date='2017-08-27T22:32:42Z',
                                        published_date='2017-08-27T22:32:39Z',
                                        category=self.post_category,
                                        image='blogimage/default.jpg',
                                        views=4, score=5)
        self.post.save()

    def test_blog_menu_item_has_class_active(self):
        post_detail = self.client.get('/blog/1/')
        print post_detail
        self.assertIn('id="nav-blog"'
                      ' class="active"', post_detail.content)

    def tearDown(self):
        self.user.delete()
        self.post.delete()
        self.post_category.delete()


class PostDetailPageVisitorUserTest(TestCase):
    """ Test blog page for visitors (not logged in) users """
    def setUp(self):
        super(PostDetailPageVisitorUserTest, self).setUp()
        self.user = User.objects.create_user(username='test@test.com',
                                             email='test@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test', is_staff='True')
        self.user.save()
        self.post_category = Category.objects.create(name='test')
        self.post_category.save()
        self.post = Post.objects.create(author=self.user, title='Test',
                                        content='Test',
                                        created_date='2017-08-27T22:32:42Z',
                                        published_date='2017-08-27T22:32:39Z',
                                        category=self.post_category,
                                        image='blogimage/default.jpg',
                                        views=4, score=5)

        self.post.save()

    def test_voting_not_shown_for_visitors(self):
        post_detail = self.client.get('/blog/1/')
        self.assertNotIn('id="voting"', post_detail.content)

    def test_login_shown_for_visitors_instead_of_voting(self):
        post_detail = self.client.get('/blog/1/')
        self.assertIn('id="login-voting"', post_detail.content)

    def test_comments_not_shown_for_visitors(self):
        post_detail = self.client.get('/blog/1/')
        self.assertNotIn('id="disqus"', post_detail.content)

    def test_login_shown_for_visitors_instead_of_comments(self):
        post_detail = self.client.get('/blog/1/')
        self.assertIn('id="login-disqus"', post_detail.content)

    def tearDown(self):
        self.user.delete()
        self.post.delete()
        self.post_category.delete()


class PostDetailPageLoggedUserTest(TestCase):
    """ Test blog page for logged users """
    def setUp(self):
        super(PostDetailPageLoggedUserTest, self).setUp()
        self.user = User.objects.create_user(username='test@test.com',
                                             email='test@test.com',
                                             password='letmein1',
                                             first_name='test',
                                             last_name='test',
                                             company='test', is_staff='True')
        self.user.save()
        self.login = self.client.login(username='test@test.com',
                                       password='letmein1')
        self.assertTrue(self.login)
        self.post_category = Category.objects.create(name='test')
        self.post_category.save()
        self.post = Post.objects.create(author=self.user, title='Test',
                                        content='Test',
                                        created_date='2017-08-27T22:32:42Z',
                                        published_date='2017-08-27T22:32:39Z',
                                        category=self.post_category,
                                        image='blogimage/default.jpg',
                                        views=4, score=5)

        self.post.save()

    def test_voting_shown_for_logged_users(self):
        post_detail = self.client.get('/blog/1/')
        self.assertIn('id="voting"', post_detail.content)

    def test_login_not_shown_for_logged_users(self):
        post_detail = self.client.get('/blog/1/')
        self.assertNotIn('id="login-voting"', post_detail.content)

    def test_comments_shown_for_logged_users(self):
        post_detail = self.client.get('/blog/1/')
        self.assertIn('id="disqus"', post_detail.content)

    def test_login_not_shown_for_logged_users_instead_of_comments(self):
        post_detail = self.client.get('/blog/1/')
        self.assertNotIn('id="login-disqus"', post_detail.content)

    def tearDown(self):
        self.user.delete()
        self.post.delete()
        self.post_category.delete()
