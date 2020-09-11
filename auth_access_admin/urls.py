"""
CC_ERP URL Configuration
"""

from django.urls import path
from . import views

app_name = "auth"

urlpatterns = [
    path("login/", views.Login_page.as_view(), name="login"),
    path("index/", views.Index.as_view(), name="index"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path(
        "accounts/password_reset/",
        views.Reset_Password.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "account/password_reset_complete/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
