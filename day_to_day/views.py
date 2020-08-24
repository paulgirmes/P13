from django.shortcuts import render,reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import gettext as _
from frontpage.models import Child_care_facility
from auth_access_admin.models import Employee, FamilyMember
from .models import Message, Child, DailyFact
from .forms import (
    DailyFactForm, SleepFormSet, MealFormSet,
    FeedingBottleFormSet, ActivityFormSet,
    MedicalEventFormSet,
)


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
    child_care_facility = Child_care_facility.objects.get(
        name__icontains=settings.STRUCTURE
        )
    extra_context = {"child_care_facility" : child_care_facility,
        }
    model = DailyFact
    template_name = "day_to_day/_trans_list.html"
    pk= None
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(child=kwargs.get(self.pk)).filter(
            time_stamp__date=timezone.now().date()
            )
        allow_empty = self.get_allow_empty()
        user = Employee.objects.get(username__contains=request.user.username)
        self.extra_context["employee"] = user
        self.extra_context["child"] = Child.objects.get(pk=kwargs.get(self.pk))
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, 'exists'):
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

class EmployeeTransmissionsListView(LoginRequiredMixin, ListView):
    child_care_facility = Child_care_facility.objects.get(name__icontains=settings.STRUCTURE)
    extra_context = {"child_care_facility" : child_care_facility,
        }
    model = DailyFact
    template_name = "day_to_day/_trans_list.html"
    def get(self, request, *args, **kwargs):
        user = Employee.objects.get(username__contains=request.user.username)
        self.object_list = self.get_queryset().filter(
                employee__username=user.username
                ).filter(
                time_stamp__date=timezone.now().date()
                )
        allow_empty = self.get_allow_empty()
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
    


class ChildTransmissionsAddView(LoginRequiredMixin, FormView):
    child_care_facility = Child_care_facility.objects.get(
                                name__icontains=settings.STRUCTURE,
                            )
    extra_context = {"child_care_facility" : child_care_facility,
        }
    template_name = "day_to_day/_trans_detail.html"
    initial = {}
    form_class = DailyFactForm
    def get(self, request, *args, **kwargs):
        user = Employee.objects.get(username__contains=request.user.username)
        self.extra_context["employee"] = user
        return self.render_to_response(self.get_context_data())


class TransmissionsChangeView(LoginRequiredMixin, FormView):
    pk =None
    child_care_facility = Child_care_facility.objects.get(
                                name__icontains=settings.STRUCTURE,
                            )
    extra_context = {"child_care_facility" : child_care_facility,
        }
    template_name = "day_to_day/_trans_detail.html"
    success_url = None
    form_class = DailyFactForm
    transmission= None
    def get(self, request, *args, **kwargs):
        user = Employee.objects.get(username__contains=request.user.username)
        self.transmission = DailyFact.objects.get(pk=kwargs.get(self.pk))
        if self.transmission.employee == user:
            self.extra_context["employee"] = user
            self.initial = {"child" : self.transmission.child, 
                        "comment" : self.transmission.comment,
                    }
            self.extra_context["trans"] = self.transmission
            self.extra_context["sleep_form"] = SleepFormSet(instance=self.transmission)
            self.extra_context["meal_form"] = MealFormSet(instance=self.transmission)
            self.extra_context["activity_form"] = ActivityFormSet(instance=self.transmission)
            self.extra_context["feeding_bttle_form"] = FeedingBottleFormSet(instance=self.transmission)
            self.extra_context["medical_form"] = MedicalEventFormSet(instance=self.transmission)
            return self.render_to_response(self.get_context_data())
        else:
            raise PermissionDenied

    def form_invalid(self, formset):
        """If the form is invalid, render the invalid form."""
        self.extra_context["message"] = "La modification de la donnée "+formset[0][1]+" n'a pas été effectuée merci de vérifier les erreurs"
        self.extra_context[formset[0][0]] = formset[1]
        return self.render_to_response(self.get_context_data())
    
    def get_formset(self, post_data, user):
        if post_data.get("sleep_set-TOTAL_FORMS"):
            form_name = ["sleep_form", "Sieste"]
            form = SleepFormSet(self.request.POST, instance=self.transmission)
        elif post_data.get("meal_set-TOTAL_FORMS"):
            form_name = ["meal_form", "Repas"]
            form = MealFormSet(self.request.POST, instance=self.transmission)
        elif post_data.get("activity_set-TOTAL_FORMS"):
            form_name = ["activity_form", "Activités"]
            form = ActivityFormSet(self.request.POST, instance=self.transmission)
        elif post_data.get("feedingbottle_set-TOTAL_FORMS"):
            form_name = ["feeding_bttle_form", "Biberons"]
            form = FeedingBottleFormSet(self.request.POST, instance=self.transmission)
        elif post_data.get("medicalevent_set-TOTAL_FORMS"):
            form_name = ["medical_form", "Médical"]
            form = MedicalEventFormSet(self.request.POST, instance=self.transmission)
        else :
            form_name = ["form", "Commentaire"]
            form = self.form_class(data={"child": self.transmission.child,
                "employee": user,
                "comment" : post_data.get("comment"),
            })
        return [form_name, form]

    def post(self, request, *args, **kwargs):
        user = Employee.objects.get(username__contains=request.user.username)
        self.transmission = DailyFact.objects.get(pk=kwargs.get(self.pk))
        if self.transmission.employee == user:
            self.transmission = DailyFact.objects.get(pk=kwargs.get(self.pk))
            self.success_url = str(self.transmission.pk)
            formset = self.get_formset(request.POST, user)

            if formset[1].is_valid() and formset[0][0]=="form" :
                self.transmission.comment = formset[1].cleaned_data["comment"]
                self.transmission.save()
                self.extra_context["message"] = "La modification a bien été enregistrée"
                return self.form_valid(formset[1])
            elif formset[1].is_valid():
                formset[1].save()
                return self.form_valid(formset[1])
            else:
                return self.form_invalid(formset)
        else:
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
