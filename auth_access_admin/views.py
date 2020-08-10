from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import Login

class Login_page(auth_views.LoginView):
    authentication_form = Login
    template_name = "auth_access_admin/login.html"


class Index(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    template_name = "auth_access_admin/index.html"

    def get(self, request, *args, **kwargs):
        extra_context = request.user
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class Logout(LoginRequiredMixin, auth_views.LogoutView):
    next_page = "/"
