from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View

from .forms import SignUpForm, PostForm, SearchForm
from .models import Post


class IndexView(View):
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        posts = Post.objects.filter(is_published=True)

        drafts = None
        if request.user is not None:
            if request.user.is_authenticated:
                drafts = Post.objects.filter(user=request.user).filter(is_published=False)

        if form.is_valid():
            category = int(form.cleaned_data.get('category'))
            tag = str(form.cleaned_data.get('tag')).strip().lower()

            if category != 0:
                posts = posts.filter(category_id=category)

            if tag.isalnum():
                posts = posts.filter(tags__contains=[tag])

            posts = posts.all()

        else:
            form = SearchForm()
            posts = posts.all().order_by('-id')

        return render(request, 'home.html', {
            'posts': posts,
            'drafts': drafts,
            'form': form
        })


class SignUpView(View):
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)

            user.save()
            return redirect('signin')
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


class AddPostView(View):
    form_class = PostForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'add_post.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category = form.cleaned_data.get('category')
            tags_data = str(form.cleaned_data.get('tags')).split(" ")
            tags = []

            for tag in tags_data:
                tag_string = tag.strip().lower()

                if len(tag_string) != 0:
                    tags.append(tag_string)

            post = Post(
                user=request.user,
                title=title,
                content=content,
                tags=tags,
                category_id=category
            )

            if request.POST.get('action', '') == 'save_draft':
                post.is_published = False

            post.save()
            return redirect('index')
        else:
            form = PostForm()
        return render(request, 'add_post.html', {'form': form})


class PostView(View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            post = None
        return render(request, 'view_post.html', {'post': post})


class PostEditView(View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            tags = ""
            for tag in post.tags:
                tag_string = tag.strip().lower()

                if len(tag_string) != 0:
                    tags = tags + tag_string + " "

            form = PostForm(initial={
                'title': post.title,
                'content': post.content,
                'tags': tags,
                'category': post.category
            })

        except ObjectDoesNotExist:
            post = None
            form = None

        return render(request, 'edit_post.html', {'form': form, 'post': post})

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category = form.cleaned_data.get('category')
            tags_data = str(form.cleaned_data.get('tags')).split(" ")
            tags = []

            for tag in tags_data:
                tag_string = tag.strip().lower()

                if len(tag_string) != 0:
                    tags.append(tag_string)

            post.title = title
            post.content = content
            post.tags = tags
            post.category_id = category

            if request.POST.get('action', '') == 'save_post':
                post.is_published = True

            post.save()

            return redirect('index')
        else:
            return render(request, 'edit_post.html', {'form': form, 'post': post})


class PostDeleteView(View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

            if request.user == post.user:
                post.delete()

        except ObjectDoesNotExist:
            post = None

        return render(request, 'delete_post.html', {'post': post})
