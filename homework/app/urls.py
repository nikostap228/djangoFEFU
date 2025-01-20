from django.urls import include, path
from . import views

urlpatterns = [
    path("get/", views.get_view, name="get"),
    path("get2/", views.get_view2, name="get2"),
    path("post/", views.post_view, name="post"),
    path("unified/", views.unified_view, name="unified"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("auth/", include("rest_framework.urls")),
]
