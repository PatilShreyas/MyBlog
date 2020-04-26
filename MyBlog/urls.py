from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import signup_view

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', signup_view, name='signup'),
    path('signin/', auth_views.LoginView.as_view(), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('new/', views.addpost_view, name='new_post'),
    path('post/<int:post_id>/', views.postview_view, name='post'),
    path('post/<int:post_id>/edit', views.postedit_view, name='editpost'),
]
