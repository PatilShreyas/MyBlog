from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase

from .models import Category, Post
from .views import index


class HomePageTest(TestCase):
    def test_blog_home_page(self):
        request = HttpRequest()
        response = index(request)

        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Blog - Home</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_posts_in_blog_home_page(self):
        # Insert post in database
        user = get_user_model().objects.create_user('test', 'test@email.com', 'test')
        category1 = Category.objects.create(name="Test Category 1")
        Post.objects.create(user=user, title="Test Title 1", content="Test Content", category=category1,
                            tags=['tag1', 'tag2'], )

        request = HttpRequest()
        response = index(request)

        html = response.content.decode('utf8')

        # Check for post's existence
        self.assertIn('Test Title 1', html)

        # Check Category name
        self.assertIn('Test Category 1', html)

    def test_auth_in_blog_home_page(self):
        user = get_user_model().objects.create_user('test', 'test@email.com', 'test')
        user.first_name = "TestName"

        request = HttpRequest()
        request.user = user

        response = index(request)

        html = response.content.decode('utf8')

        # Check for user's existence
        self.assertIn('TestName', html)

        # Check for signout button
        self.assertIn('Sign Out', html)
