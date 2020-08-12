from django.shortcuts import render, reverse
from django.views.generic import FormView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import Login, Password_reset_form

class Login_page(auth_views.LoginView):
    authentication_form = Login
    template_name = "auth_access_admin/_login.html"


class Index(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    template_name = "auth_access_admin/_index.html"

    def get(self, request, *args, **kwargs):
        extra_context = request.user
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class Logout(LoginRequiredMixin, auth_views.LogoutView):
    next_page = "/"

class Reset_Password(auth_views.PasswordResetView):
    template_name = "auth_access_admin/_forgot-password.html"
    email_template_name = "auth_access_admin/password_reset_email.html"
    success_url = reverse_lazy("auth:password_reset_done")


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "auth_access_admin/_password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "auth_access_admin/_password_reset_confirm.html"
    form_class = Password_reset_form
    success_url = reverse_lazy("auth:password_reset_complete")

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "auth_access_admin/_password_reset_complete.html"