from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    TemplateView, ListView, DetailView,
    FormView, CreateView,
)
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
    child_care_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
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
                user = Employee.objects.get(username=request.user.username)
                self.extra_context["employee"] = user
                return self.render_to_response(self.get_context_data())
        except:
            raise PermissionDenied


class ChildListView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    child_care_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
    model = Child
    template_name = "day_to_day/_child_list.html"
    extra_context = {"child_care_facility" : child_care_facility,
        }
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        user = Employee.objects.get(username=request.user.username)
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
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    child_care_facility = Child_care_facility.objects.get(
        name=settings.STRUCTURE
        )
    extra_context = {"child_care_facility" : child_care_facility,
        }
    model = DailyFact
    template_name = "day_to_day/_trans_list.html"

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(child=kwargs.get("pk")).filter(
            time_stamp__date=timezone.now().date()
            ).order_by("-time_stamp")
        allow_empty = self.get_allow_empty()
        user = Employee.objects.get(username=request.user.username)
        self.extra_context["employee"] = user
        self.extra_context["child"] = Child.objects.get(pk=kwargs.get("pk"))
        if kwargs.get("success", False)== "True":
            self.extra_context["transmission_recorded"]="votre transmission a bien été enregistrée"
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
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    child_care_facility = Child_care_facility.objects.get(
                                name=settings.STRUCTURE,
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
        user = Employee.objects.get(username=request.user.username)
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
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    child_care_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
    extra_context = {"child_care_facility" : child_care_facility,
        }
    model = DailyFact
    template_name = "day_to_day/_trans_list.html"
    def get(self, request, *args, **kwargs):
        user = Employee.objects.get(username=request.user.username)
        self.object_list = self.get_queryset().filter(
                employee=user.username
                ).filter(
                time_stamp__date=timezone.now().date()
                ).order_by("-time_stamp")
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


class ChildTransmissionsAddView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    child_care_facility = Child_care_facility.objects.get(
                                name__icontains=settings.STRUCTURE,
                            )
    extra_context = {"child_care_facility" : child_care_facility,
        }
    template_name = "day_to_day/_trans_add.html"
    form_class = DailyFactForm
    success_url = None

    def get(self, request, *args, **kwargs):
        if self.extra_context.get("post")==True:
            self.extra_context["post"]=False
        else:
            self.extra_context["message"]=None
        self.child = Child.objects.get(pk=kwargs.get("pk"))
        self.user = Employee.objects.get(username__contains=request.user.username)
        self.extra_context["employee"] = self.user
        self.extra_context["child"] = self.child
        self.extra_context["sleep_form"] = SleepFormSet()
        self.extra_context["meal_form"] = MealFormSet()
        self.extra_context["activity_form"] = ActivityFormSet()
        self.extra_context["feeding_bttle_form"] = FeedingBottleFormSet()
        self.extra_context["medical_form"] = MedicalEventFormSet()
        self.object = None
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.user = Employee.objects.get(username__contains=request.user.username)
        self.object = None
        self.child = Child.objects.get(pk=kwargs.get("pk"))
        self.extra_context["post"]=True
        self.success_url=reverse("d_to_d:Child_transmissions", args=(self.child.pk, True), current_app=self.request.resolver_match.namespace)
        form = self.form_class(data={"child": self.child,
                    "employee": self.user,
                    "comment" : request.POST.get("comment"),
                })
        if form.is_valid():
            new_transmission = form.save()
            formlist = [
                (SleepFormSet(request.POST, instance=new_transmission), ["sleep_form", "Sieste"]),
                (MealFormSet(request.POST, instance=new_transmission), ["meal_form", "Repas"]),
                (ActivityFormSet(request.POST, instance=new_transmission), ["activity_form", "Activités"]),
                (FeedingBottleFormSet(request.POST, instance=new_transmission), ["feeding_bttle_form", "Biberons"]),
                (MedicalEventFormSet(request.POST, instance=new_transmission), ["medical_form", "Médical"]),
            ]
            error=[]
            for formset, formset_name in formlist:
                #commit=False won't allow to save the instance of formset...thus formset.save() and .delete if any errors
                if formset.is_valid():
                    pass
                else:
                    self.extra_context[formset_name[0]] = formset
                    error.append(formset_name[1])
            if error:
                new_transmission.delete()
                self.extra_context["message"] = "Veuillez corriger les erreurs dans les champs suivants : "+ ", ".join(error)
                return self.render_to_response(self.get_context_data(form=form))
            else:
                for formset, formset_name in formlist:
                    formset.save()
                return self.form_valid(form)
        else:
            self.extra_context["message"] = "Veuillez corriger les erreurs dans le commentaire"
            return self.form_invalid(form)


class TransmissionsChangeView(LoginRequiredMixin, FormView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    pk = None
    child_care_facility = Child_care_facility.objects.get(
                                name__icontains=settings.STRUCTURE,
                            )
    extra_context = {"child_care_facility" : child_care_facility,
        "success":None,
        }
    template_name = "day_to_day/_trans_detail.html"
    success_url = None
    form_class = DailyFactForm
    def get(self, request, *args, **kwargs):
        if self.extra_context["success"]==True:
            self.extra_context["success"]=False
            self.extra_context["transmission_recorded"] = "Votre Modification a bien été enregistrée"
            self.extra_context["message"] = None
        else:
            self.extra_context["transmission_recorded"] = None
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
        self.initial = {"child" : self.transmission.child, 
            "comment" : self.transmission.comment,
        }
        form = self.form_class(initial=self.initial)
        self.extra_context["form"]=form
        return self.render_to_response(self.get_context_data())
    
    def get_formset(self, post_data, user):
        if post_data.get("sleep_set-TOTAL_FORMS"):
            form_name = ["sleep_form", "Sieste"]
            form = SleepFormSet(post_data, instance=self.transmission)
        elif post_data.get("meal_set-TOTAL_FORMS"):
            form_name = ["meal_form", "Repas"]
            form = MealFormSet(post_data, instance=self.transmission)
        elif post_data.get("activity_set-TOTAL_FORMS"):
            form_name = ["activity_form", "Activités"]
            form = ActivityFormSet(post_data, instance=self.transmission)
        elif post_data.get("feedingbottle_set-TOTAL_FORMS"):
            form_name = ["feeding_bttle_form", "Biberons"]
            form = FeedingBottleFormSet(post_data, instance=self.transmission)
        elif post_data.get("medicalevent_set-TOTAL_FORMS"):
            form_name = ["medical_form", "Médical"]
            form = MedicalEventFormSet(post_data, instance=self.transmission)
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
        self.success_url = str(self.transmission.pk)
        if self.transmission.employee == user:
            formset = self.get_formset(request.POST, user)

            if formset[1].is_valid() and formset[0][0]=="form" :
                self.transmission.comment = formset[1].cleaned_data["comment"]
                self.transmission.save()
                self.extra_context["success"]=True
                self.transmission = DailyFact.objects.get(pk=self.transmission.pk)
                return self.form_valid(self.form_class())
            elif formset[1].is_valid():
                formset[1].save()
                self.extra_context["success"]=True
                return self.form_valid(self.form_class())
            else:
                self.extra_context["success"]=False
                return self.form_invalid(formset)
        else:
            raise PermissionDenied
    

class ParentView(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    child_care_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    extra_context = {"child_care_facility" : child_care_facility,
        }
    template_name = "day_to_day/_parent_trans_list.html"
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        try: 
            user = FamilyMember.objects.get(username=request.user.username)
            childs = Child.objects.filter(relative=user)
            # transmissions = DailyFact.objects.filter(child=childs)
            self.extra_context["parent"] = user
            self.extra_context["childs"] = childs
            return self.render_to_response(self.get_context_data())
        except:
            if request.user.is_superuser:
                return self.render_to_response(self.get_context_data())
            raise PermissionDenied

class Child_transmissions_report(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'
    child_care_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
    extra_context = {"child_care_facility" : child_care_facility,
        }
    model = DailyFact
    template_name = "day_to_day/_parent_child_trans_list.html"
    def get(self, request, *args, **kwargs):
        try:
            user = FamilyMember.objects.get(username=request.user.username)
        except:
            if request.user.is_superuser:
                pass
            raise PermissionDenied
        self.object_list = self.get_queryset().filter(
                child = self.kwargs.get("pk")
                ).order_by("-time_stamp")
        allow_empty = self.get_allow_empty()
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
        self.extra_context["child"]= Child.objects.get(pk=self.kwargs.get("pk"))
        context = self.get_context_data()
        return self.render_to_response(context)