import datetime
from django.shortcuts import reverse, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.generic import TemplateView
from django.contrib.auth import login as auth_login, views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from frontpage.models import Child_care_facility
from day_to_day.models import Child, MedicalEvent, DailyFact
from django.conf import settings
from .models import Employee, FamilyMember

from .forms import Login, Password_reset_form


class Login_page(auth_views.LoginView):
    authentication_form = Login
    template_name = "auth_access_admin/_login.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        try:
            dailyfact_access = FamilyMember.objects.get(
                username=user.username
            ).has_daylyfact_access
        except ObjectDoesNotExist:
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        if dailyfact_access:
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise PermissionDenied


class Index(LoginRequiredMixin, TemplateView):
    template_name = "auth_access_admin/_index.html"
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        try:
            self.child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context[
                "child_care_facility"
            ] = self.child_care_facility
            childs = Child.objects.filter(
                cc_facility__name=self.child_care_facility
            )
            child_number = childs.count()
            self.extra_context["fill_ratio"] = int(
                child_number / self.child_care_facility.max_child_number * 100
            )
            events_today = DailyFact.objects.filter(
                    time_stamp__date=datetime.datetime.now().date()
                ).filter(child__cc_facility=self.child_care_facility)

            medical_event_today = MedicalEvent.objects.filter(
                daily_fact__time_stamp__date=datetime.datetime.now().date()
            ).filter(daily_fact__child__cc_facility=self.child_care_facility)
            self.extra_context.update(
                {
                    "child_number": child_number,
                    "events_today": len(events_today),
                    "medical_event_today": medical_event_today.count(),
                }
            )
        except ObjectDoesNotExist:
            self.extra_context.update(
                {
                    "child_number": None,
                    "events_today": None,
                    "medical_event_today": None,
                    "child_care_facility": None,
                    "fill_ratio": None,
                }
            )
        try:
            if request.user.is_superuser:
                self.extra_context["employee"] = request.user
                return self.render_to_response(self.get_context_data())
            else:
                user = Employee.objects.get(
                    username=request.user.username,
                )
                if user.Is_manager:
                    self.extra_context["employee"] = user
                    return self.render_to_response(self.get_context_data())
                else:
                    self.extra_context["employee"] = user
                    return redirect(reverse("d_to_d:employee"))
        except ObjectDoesNotExist:
            user = FamilyMember.objects.get(username=request.user.username)
            if user.has_daylyfact_access:
                self.extra_context["parent"] = user
                return redirect(reverse("d_to_d:parent"))
            else:
                raise PermissionDenied


class Logout(LoginRequiredMixin, auth_views.LogoutView):
    next_page = "frontpage:homepage"


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
