from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import gettext as _
from frontpage.models import Child_care_facility
from auth_access_admin.models import Employee, FamilyMember
from .models import Message, Child, DailyFact


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


class ChildListView(LoginRequiredMixin, ListView):
    child_care_facility = Child_care_facility.objects.get(name__icontains=settings.STRUCTURE)
    model = Child
    template_name = "day_to_day/_child_list.html"
    extra_context = {"child_care_facility" : child_care_facility,
        }
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        user = Employee.objects.get(username__contains=request.user.username)
        self.extra_context["employee"] = user

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)


class ChildTransmissionsView(LoginRequiredMixin, ListView):
    child_care_facility = Child_care_facility.objects.get(name__icontains=settings.STRUCTURE)
    extra_context = {"child_care_facility" : child_care_facility,
        }
    model = DailyFact
    template_name = "day_to_day/_trans_list.html"
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(child=kwargs.get(pk))
        allow_empty = self.get_allow_empty()
        user = Employee.objects.get(username__contains=request.user.username)
        self.extra_context["employee"] = user

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)


class ChildView(LoginRequiredMixin, DetailView):
    child_care_facility = Child_care_facility.objects.get(
                                name__icontains=settings.STRUCTURE,
                            )
    model = Child
    template_name = "day_to_day/_child_detail.html"
    emergency_contacts = FamilyMember.objects.filter(
                            family_link__emergency_contact_person=True,
                        )
    authorized_familly = FamilyMember.objects.filter(
                            family_link__retrieval_auth=True,
                        )
    extra_context = {"child_care_facility" : child_care_facility,
        }
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = Employee.objects.get(username__contains=request.user.username)
        self.extra_context["employee"] = user
        self.extra_context["emergency_contacts"] = self.emergency_contacts.filter(
                family_link__child=self.object
                )
        self.extra_context["authorized_familly"] = self.authorized_familly.filter(
                family_link__child=self.object
                )
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class TransmissionsListView(LoginRequiredMixin, ListView):
    model = DailyFact
    template_name = "day_to_day/_trans_list.html"


class ChildTransmissionsAddView(LoginRequiredMixin, TemplateView):
    pass


class ChildTransmissionsChangeView(LoginRequiredMixin, TemplateView):
    pass


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
