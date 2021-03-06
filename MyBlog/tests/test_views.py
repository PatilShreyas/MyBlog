from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase

from MyBlog.models import Category, Post
from MyBlog.views import index, postdelete_view, postedit_view, postview_view


class IndexPageTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('test', 'test@email.com', 'test')

    def test_blog_home_page(self):
        request = HttpRequest()
        request.user = self.user
        response = index(request)

        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Blog - Home</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_posts_in_blog_home_page(self):
        # Insert post in database
        category1 = Category.objects.create(name="Test Category 1")
        Post.objects.create(user=self.user, title="Test Title 1", content="Test Content", category=category1,
                            tags=['tag1', 'tag2'], )

        request = HttpRequest()
        request.user = self.user

        response = index(request)

        html = response.content.decode('utf8')

        # Check for post's existence
        self.assertIn('Test Title 1', html)

        # Check Category name
        self.assertIn('Test Category 1', html)

    def test_auth_in_blog_home_page(self):
        user = get_user_model().objects.create_user('testauth', 'testauth@email.com', 'testauth')
        user.first_name = "MyTestFirstName"

        request = HttpRequest()
        request.user = user

        response = index(request)

        html = response.content.decode('utf8')

        # Check for user's existence
        self.assertIn('MyTestFirstName', html)

        # Check for signout button
        self.assertIn('Sign Out', html)


class PostDeleteViewTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user('test1', 'test1@email.com', 'test1')
        self.user2 = get_user_model().objects.create_user('test2', 'test2@email.com', 'test2')

        # Insert post in database
        self.category1 = Category.objects.create(name="Test Category 1")
        self.post = Post.objects.create(user=self.user1, title="Test Title 1", content="Test Content",
                                        category=self.category1,
                                        tags=['tag1', 'tag2'], )

    def test_post_deleted_in_post_delete_page(self):
        request = HttpRequest()
        request.user = self.user1
        response = postdelete_view(request, self.post.id)

        html = response.content.decode('utf8')

        # Check for post is deleted text
        self.assertIn('Post has been deleted!', html)

    def test_unauth_in_post_view_page(self):
        request = HttpRequest()
        request.user = self.user2
        response = postdelete_view(request, self.post.id)

        html = response.content.decode('utf8')

        # Check if edit button not exists
        self.assertIn('ACCESS DENIED', html)


class PostViewEditTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user('test1', 'test1@email.com', 'test1')
        self.user2 = get_user_model().objects.create_user('test2', 'test2@email.com', 'test2')

        # Insert post in database
        self.category1 = Category.objects.create(name="Test Category 1")
        self.post1 = Post.objects.create(user=self.user1, title="Test Title 1", content="Test Content",
                                         category=self.category1,
                                         tags=['tag1', 'tag2'], )
        self.post2 = Post.objects.create(user=self.user1, title="Test Title 2", content="Test Content",
                                         category=self.category1,
                                         tags=['tag1', 'tag2'], is_published=False)

    def test_unauth_in_post_edit_page(self):
        request = HttpRequest()
        request.user = self.user2
        response = postedit_view(request, self.post1.id)

        html = response.content.decode('utf8')

        # Check if it shows access denied
        self.assertIn("ACCESS DENIED!", html)

    def test_auth_in_post_edit_page(self):
        request = HttpRequest()
        request.user = self.user1
        response = postedit_view(request, self.post1.id)

        html = response.content.decode('utf8')

        # Check if publish buttons exists
        self.assertIn('Publish', html)

        # Check if save draft button not exists
        self.assertNotIn('Save Draft', html)

    def test_draft_in_post_edit_page(self):
        request = HttpRequest()
        request.user = self.user1
        response = postedit_view(request, self.post2.id)

        html = response.content.decode('utf8')

        # Check if publish buttons exists
        self.assertIn('Publish', html)

        # Check if save draft button not exists
        self.assertIn('Save draft', html)


class PostViewTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user('test1', 'test1@email.com', 'test1')
        self.user2 = get_user_model().objects.create_user('test2', 'test2@email.com', 'test2')

        # Insert post in database
        self.category1 = Category.objects.create(name="Test Category 1")
        self.post = Post.objects.create(user=self.user1, title="Test Title 1", content="Test Content",
                                        category=self.category1,
                                        tags=['tag1', 'tag2'], )

    def test_post_in_post_view_page(self):
        request = HttpRequest()

        response = postview_view(request, self.post.id)

        html = response.content.decode('utf8')

        # Check for post's existence
        self.assertIn('Test Title 1', html)

        # Check Category name
        self.assertIn('Test Category 1', html)

        # Check content
        self.assertIn('Test Content', html)

    def test_unauth_in_post_view_page(self):
        request = HttpRequest()
        request.user = self.user2
        response = postview_view(request, self.post.id)

        html = response.content.decode('utf8')

        # Check if edit button not exists
        self.assertNotIn('Edit</a>', html)

        # Check if delete button not exists
        self.assertNotIn('Delete</a>', html)

    def test_auth_in_post_view_page(self):
        request = HttpRequest()
        request.user = self.user1
        response = postview_view(request, self.post.id)

        html = response.content.decode('utf8')

        # Check if edit button exists
        self.assertIn('Edit</a>', html)

        # Check if delete button exists
        self.assertIn('Delete</a>', html)

    def test_no_post_in_post_view_page(self):
        request = HttpRequest()
        request.user = self.user1
        response = postview_view(request, 99)

        html = response.content.decode('utf8')

        # Check if edit button exists
        self.assertIn('No post!', html)
