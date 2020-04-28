from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import AddPostView, SignUpView, IndexView, PostView, PostEditView, PostDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', auth_views.LoginView.as_view(), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('new/', login_required(AddPostView.as_view(), login_url='/blog/signin/'), name='new_post'),
    path('post/<int:post_id>/', PostView.as_view(), name='post'),
    path('post/<int:post_id>/edit/', PostEditView.as_view(), name='editpost'),
    path('post/<int:post_id>/delete/', PostDeleteView.as_view(), name='deletepost'),
]
