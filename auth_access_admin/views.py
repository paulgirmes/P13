from django.shortcuts import render, reverse, redirect
from django.core.exceptions import PermissionDenied
from django.views.generic import FormView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from frontpage.models import Child_care_facility
from settings import STRUCTURE
from .models import Employee, FamilyMember

from .forms import Login, Password_reset_form

class Login_page(auth_views.LoginView):
    authentication_form = Login
    template_name = "auth_access_admin/_login.html"
    

class Index(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    # template_name = "auth_access_admin/_index.html"
    child_care_facility = Child_care_facility.objects.get(name__icontains=STRUCTURE)
    extra_context = {"child_care_facility" : child_care_facility}

    def get(self, request, *args, **kwargs):
        try:
            user = Employee.objects.get(username__contains=request.user.username)
            if user.Is_manager:
                self.extra_context["employee"] = user
                self.template_name = "auth_access_admin/_index.html"
                return self.render_to_response(self.get_context_data())
            else:
                redirect(reverse("day_to_day:index"))
        except:
            try: 
                user = FamilyMember.objects.get(username__contains=request.user.username)
                if user.Is_parent:
                    self.extra_context["parent"] = user
                    redirect(reverse("day_to_day:index"))
            except:
                raise PermissionDenied



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