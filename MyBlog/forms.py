from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Category, Post


class SearchForm(forms.Form):
    categories = Category.objects.all()

    category_choice = [(0, "All")]
    for category in categories:
        category_choice.append((category.id, str(category.name)))

    category = forms.ChoiceField(choices=category_choice)
    tag = forms.CharField(max_length=10, required=False)

    class Meta:
        model = Post
        fields = ('category', 'tags')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)


class SignInForm(AuthenticationForm):
    username = forms.CharField(max_length=30)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'password',)


class NewPostForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
    tags = forms.CharField(max_length=30, required=True)

    categories = Category.objects.all()
    category = forms.ChoiceField(choices=[(category.id, str(category.name)) for category in categories])

    class Meta:
        model = Post
        fields = ('title', 'content', 'tags', 'category',)
