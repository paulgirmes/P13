import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.core.exceptions import PermissionDenied
from django.views.generic import FormView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from frontpage.models import Child_care_facility
from day_to_day.models import Child, MedicalEvent, DailyFact
from django.conf import settings
from .models import Employee, FamilyMember

from .forms import Login, Password_reset_form

class Login_page(auth_views.LoginView):
    authentication_form = Login
    template_name = "auth_access_admin/_login.html"
    

class Index(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    child_number = Child.objects.all().count()
    child_care_facility = Child_care_facility.objects.get(name__icontains=settings.STRUCTURE)
    events_today = DailyFact.objects.filter(time_stamp__date=datetime.datetime.now().date())
    medical_event_today = MedicalEvent.objects.filter(daily_fact__time_stamp__date=datetime.datetime.now().date())
    extra_context = {"child_care_facility" : child_care_facility,
        "child_number" : child_number,
        "fill_ratio" : int(child_number/child_care_facility.max_child_number*100),
        "events_today" : events_today.count(),
        "medical_event_today": medical_event_today.count(),
        }
    template_name = "auth_access_admin/_index.html"
    
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                self.extra_context["employee"] = request.user
                return self.render_to_response(self.get_context_data())
            else:
                user = Employee.objects.get(username=request.user.username)
                if user.Is_manager:
                    self.extra_context["employee"] = user
                    return self.render_to_response(self.get_context_data())
                else:
                    self.extra_context["employee"] = user
                    return redirect(reverse("d_to_d:employee"))
        except:
                user = FamilyMember.objects.get(username=request.user.username)
                if user.has_daylyfact_access:
                    self.extra_context["parent"] = user
                    return redirect(reverse("d_to_d:parent"))
                else:
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