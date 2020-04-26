import json

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from MyBlog.models import Post, Category


class ListAPITest(APITestCase):
    posts_url = '/api/posts/'
    category_url = '/api/category/'

    def setUp(self):
        user = get_user_model().objects.create_user('test', 'test@email.com', 'test')

        self.category1 = Category.objects.create(name="Test Category 1")

        self.post = Post.objects.create(user=user, title="Test Title 1", content="Test Content",
                                        category=self.category1,
                                        tags=['tag1', 'tag2'], )

    def test_get_categories(self):
        response = self.client.get(self.category_url)

        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [
                {'id': self.category1.id, 'name': self.category1.name},
            ]
        )

    def test_get_posts(self):
        response = self.client.get(self.posts_url)
        json_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(json_data[0]['title'], "Test Title 1")
        self.assertEqual(json_data[0]['content'], "Test Content")
        self.assertEqual(json_data[0]['tags'], ['tag1', 'tag2'])
