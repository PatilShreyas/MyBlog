from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.TextField()


class Post(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

