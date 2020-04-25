from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # For API authentication
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
