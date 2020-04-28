from django.contrib.auth import get_user_model
from django.test import TestCase

from MyBlog.models import Category, Post


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='CategoryTest')

    def test_category_name(self):
        category = Category.objects.get(id=self.category.id)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')


class PostModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('test2', 'test2@email.com', 'test2')
        category1 = Category.objects.create(name="Test Category 1")
        self.post = Post.objects.create(user=user, title="Test Title 1", content="Test Content",
                            category=category1,
                            tags=['tag1', 'tag2'], )

    def test_category_name(self):
        post = Post.objects.get(id=self.post.id)
        field_user = post._meta.get_field('user').verbose_name
        field_title = post._meta.get_field('title').verbose_name
        field_content = post._meta.get_field('content').verbose_name
        field_category = post._meta.get_field('category').verbose_name
        field_tags = post._meta.get_field('tags').verbose_name

        self.assertEquals(field_user, 'user')
        self.assertEquals(field_title, 'title')
        self.assertEquals(field_content, 'content')
        self.assertEquals(field_category, 'category')
        self.assertEquals(field_tags, 'tags')
