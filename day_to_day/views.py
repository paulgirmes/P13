from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.exceptions import PermissionDenied
from frontpage.models import Child_care_facility
from auth_access_admin.models import Employee, FamilyMember
from .models import Message

class EmployeeView(LoginRequiredMixin, TemplateView):
    child_care_facility = Child_care_facility.objects.get(name__icontains=settings.STRUCTURE)
    messages = Message.objects.all()
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    extra_context = {"child_care_facility" : child_care_facility,
        "messages" : messages,
        }
    template_name = "day_to_day/_employee_index.html"
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                self.extra_context["employee"] = request.user
                return self.render_to_response(self.get_context_data())
            else:
                user = Employee.objects.get(username__contains=request.user.username)
                self.extra_context["employee"] = user
                return self.render_to_response(self.get_context_data())
        except:
            raise PermissionDenied


class ParentView(LoginRequiredMixin, TemplateView):
    child_care_facility = Child_care_facility.objects.get(name__icontains=settings.STRUCTURE)
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    extra_context = {"child_care_facility" : child_care_facility,
        }
    template_name = "day_to_day/_parents_index.html"
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        try: 
            user = FamilyMember.objects.get(username__contains=request.user.username)
            if user.Is_parent:
                self.extra_context["parent"] = user
                return self.render_to_response(self.get_context_data())
            else:
                raise PermissionDenied
        except:
                raise PermissionDenied
