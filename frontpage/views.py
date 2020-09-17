"""
views for frontpage application
"""

from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Child_care_facility, New
from auth_access_admin.models import FamilyMember
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from day_to_day.views import get_permission


def page_not_found_view(request, exception=None):
    return render(request, "frontpage/_404.html", status=404)


def error_view(request, exception=None):
    return render(request, "frontpage/_500.html", status=500)


class HomePage(TemplateView):
    template_name = "frontpage/_index.html"

    def get(self, request, *args, **kwargs):
        try:
            cc_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            news = list(
                New.objects.filter(cc_facility=cc_facility).order_by(
                    "date_time"
                )
            )
            self.extra_context = {
                "child_care_facility": cc_facility,
                "news": news[:4],
                "gg_adress": cc_facility.address.gg_adress_format(),
            }
        except ObjectDoesNotExist:
            self.extra_context = {
                "child_care_facility": None,
                "news": None,
                "gg_adress": None,
            }
        try:
            user = FamilyMember.objects.get(username=request.user.username)
            self.extra_context["familly_member"] = user
        except (ObjectDoesNotExist, AttributeError):
            try:
                user = get_permission(self, request)
                self.extra_context["familly_member"] = user
            except (ObjectDoesNotExist, AttributeError, PermissionDenied):
                return self.render_to_response(self.get_context_data())
        return self.render_to_response(self.get_context_data())


class Legal(TemplateView):
    template_name = "frontpage/_legal.html"

    def get(self, request, *args, **kwargs):
        try:
            cc_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
                )
            self.extra_context = {
                "child_care_facility": cc_facility,
            }
        except ObjectDoesNotExist:
            self.extra_context = {
                "child_care_facility": None,
            }
        try:
            user = FamilyMember.objects.get(username=request.user.username)
            self.extra_context["user"] = user
        except (ObjectDoesNotExist, AttributeError):
            try:
                user = get_permission(self, request)
                self.extra_context["user"] = user
            except (ObjectDoesNotExist, AttributeError, PermissionDenied):
                return self.render_to_response(self.get_context_data())
        return self.render_to_response(self.get_context_data())
