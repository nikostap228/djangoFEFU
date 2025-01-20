from django.urls import path, include
from . import views

urlpatterns = [
    path("get/", views.get_view, name="get"),
    path("get2/", views.get_view2, name="get2"),
    path("post/", views.post_view, name="post"),
    path("user/", views.user_crud, name="user_crud"),
    path("auth/", include("rest_framework.urls")),  # Для аутентификации
    path("unified/", views.unified_view, name="unified"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("user/<int:pk>/", views.user_crud, name="user_detail"),
    path(
        "reset-password/", views.reset_password_request, name="reset_password_request"
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        views.reset_password_confirm,
        name="reset_password_confirm",
    ),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path('profile/', views.profile_view, name='profile'),
]
