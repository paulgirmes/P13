"""
Views definition for day_to_day application
"""


from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView,
    CreateView,
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
    DailyFactForm,
    SleepFormSet,
    MealFormSet,
    FeedingBottleFormSet,
    ActivityFormSet,
    MedicalEventFormSet,
)


def get_permission(instance, request):
    """
    takes an instance of a view and a request, returns a user object if
    user is superuser or user is an employee
    raises permission denied if any other user
    """
    if request.user.is_superuser:
        instance.extra_context["employee"] = request.user
        return request.user
    else:
        try:
            user = Employee.objects.get(username=request.user.username)
            instance.extra_context["employee"] = user
            return user
        except ObjectDoesNotExist:
            raise PermissionDenied


class EmployeeView(LoginRequiredMixin, TemplateView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    template_name = "day_to_day/_employee_index.html"

    def get(self, request, *args, **kwargs):
        self.messages = Message.objects.filter(
            cc_facility__name=settings.STRUCTURE
        )
        self.extra_context = {"messages": self.messages}
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context["child_care_facility"] = child_care_facility
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        get_permission(instance=self, request=request)
        return self.render_to_response(self.get_context_data())


class ChildListView(LoginRequiredMixin, ListView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    model = Child
    template_name = "day_to_day/_child_list.html"

    def get(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context = {"child_care_facility": child_care_facility}
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        if child_care_facility:
            self.object_list = self.get_queryset().filter(
                cc_facility=child_care_facility
                )
        else:
            self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        get_permission(instance=self, request=request)
        context = self.get_context_data()
        return self.render_to_response(context)


class ChildTransmissionsView(LoginRequiredMixin, ListView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    model = DailyFact
    template_name = "day_to_day/_trans_list.html"

    def get(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context = {"child_care_facility": child_care_facility}
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        # redefinition of get_queryset to include only daylifacts
        # for a child and for present day
        self.object_list = (
            self.get_queryset()
            .filter(child=kwargs.get("pk"))
            .filter(time_stamp__date=timezone.now().date())
            .order_by("-time_stamp")
        )
        allow_empty = self.get_allow_empty()
        self.extra_context["child"] = Child.objects.get(pk=kwargs.get("pk"))
        # checking if a new daily fact has been successfully recorded
        if kwargs.get("success", False) == "True":
            self.extra_context[
                "transmission_recorded"
            ] = "votre transmission a bien été enregistrée"
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        get_permission(instance=self, request=request)
        return self.render_to_response(self.get_context_data())


class ChildView(LoginRequiredMixin, DetailView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    model = Child
    template_name = "day_to_day/_child_detail.html"
    emergency_contacts = FamilyMember.objects.filter(
        family_link__emergency_contact_person=True,
    )
    authorized_familly = FamilyMember.objects.filter(
        family_link__retrieval_auth=True,
    )

    def get(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context = {"child_care_facility": child_care_facility}
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        self.object = self.get_object()
        self.extra_context[
            "emergency_contacts"
        ] = self.emergency_contacts.filter(family_link__child=self.object)
        self.extra_context[
            "authorized_familly"
        ] = self.authorized_familly.filter(family_link__child=self.object)
        get_permission(instance=self, request=request)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class EmployeeTransmissionsListView(LoginRequiredMixin, ListView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    model = DailyFact
    template_name = "day_to_day/_employee_trans_list.html"

    def get(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context = {"child_care_facility": child_care_facility}
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        user = get_permission(instance=self, request=request)
        self.extra_context["employee"] = user
        if user.is_superuser:
            self.object_list = self.get_queryset().order_by("-time_stamp")
        else:
            self.object_list = (
                self.get_queryset()
                .filter(employee=user)
                .filter(time_stamp__date=timezone.now().date())
                .order_by("-time_stamp")
            )
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        return self.render_to_response(self.get_context_data())


class ChildTransmissionsAddView(LoginRequiredMixin, CreateView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    template_name = "day_to_day/_trans_add.html"
    form_class = DailyFactForm
    success_url = None
    extra_context = {}

    def get(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context = {"child_care_facility": child_care_facility}
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        # checking if a post request was just made/
        # reseting mesage if not
        if self.extra_context.get("post"):
            self.extra_context["post"] = False
        else:
            self.extra_context["message"] = None
        self.child = Child.objects.get(pk=kwargs.get("pk"))
        self.extra_context["child"] = self.child
        self.extra_context["sleep_form"] = SleepFormSet()
        self.extra_context["meal_form"] = MealFormSet()
        self.extra_context["activity_form"] = ActivityFormSet()
        self.extra_context["feeding_bttle_form"] = FeedingBottleFormSet()
        self.extra_context["medical_form"] = MedicalEventFormSet()
        self.object = None
        get_permission(instance=self, request=request)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context = {"child_care_facility": child_care_facility}
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        self.user = get_permission(instance=self, request=request)
        self.object = None
        self.child = Child.objects.get(pk=kwargs.get("pk"))
        self.extra_context["child"] = self.child
        self.extra_context["post"] = True
        self.success_url = reverse(
            "d_to_d:Child_transmissions",
            args=(self.child.pk, True),
            current_app="d_to_d",
        )
        form = self.form_class(
            data={
                "child": self.child,
                "employee": self.user,
                "comment": request.POST.get("comment"),
            }
        )
        if form.is_valid():
            # commit=False won't allow to save the instance of formset
            # (no instance is really existing)
            # thus form.save() and .delete() if any errors in any formset
            new_transmission = form.save()
            formlist = [
                (
                    SleepFormSet(request.POST, instance=new_transmission),
                    ["sleep_form", "Sieste"],
                ),
                (
                    MealFormSet(request.POST, instance=new_transmission),
                    ["meal_form", "Repas"],
                ),
                (
                    ActivityFormSet(request.POST, instance=new_transmission),
                    ["activity_form", "Activités"],
                ),
                (
                    FeedingBottleFormSet(
                        request.POST, instance=new_transmission
                    ),
                    ["feeding_bttle_form", "Biberons"],
                ),
                (
                    MedicalEventFormSet(
                        request.POST, instance=new_transmission
                    ),
                    ["medical_form", "Médical"],
                ),
            ]
            error = []
            # checking if error in any formset
            for formset, formset_name in formlist:
                if formset.is_valid():
                    self.extra_context[formset_name[0]] = formset
                else:
                    self.extra_context[formset_name[0]] = formset
                    error.append(formset_name[1])
            if error:
                new_transmission.delete()
                self.extra_context["message"] = (
                    "Veuillez corriger les erreurs dans les champs suivants : "
                    + ", ".join(error)
                )
                self.extra_context["post"] = True
                return self.render_to_response(
                    self.get_context_data()
                )
            else:
                for formset, formset_name in formlist:
                    formset.save()
                return HttpResponseRedirect(self.success_url)
        else:
            self.extra_context[
                "message"
            ] = "Veuillez corriger les erreurs dans le commentaire"
            return self.form_invalid(form)


class TransmissionsChangeView(LoginRequiredMixin, FormView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    pk = None
    extra_context = {"success": False}
    template_name = "day_to_day/_trans_detail.html"
    success_url = None
    form_class = DailyFactForm

    def get(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context["child_care_facility"] = child_care_facility
        except ObjectDoesNotExist:
            self.extra_context["child_care_facility"] = child_care_facility
        user = get_permission(instance=self, request=request)
        # checking if any post request was just made
        if self.extra_context["success"]:
            self.extra_context["success"] = False
            self.extra_context[
                "transmission_recorded"
            ] = "Votre Modification a bien été enregistrée"
            self.extra_context["message"] = None
        else:
            self.extra_context["transmission_recorded"] = None
        self.transmission = DailyFact.objects.get(pk=kwargs.get("pk"))
        # checking if the user is the author of dailifact
        # (modification only allowed by author)
        if self.transmission.employee == user or user.is_superuser:
            self.initial = {
                "child": self.transmission.child,
                "comment": self.transmission.comment,
            }
            self.extra_context["trans"] = self.transmission
            self.extra_context["sleep_form"] = SleepFormSet(
                instance=self.transmission
            )
            self.extra_context["meal_form"] = MealFormSet(
                instance=self.transmission
            )
            self.extra_context["activity_form"] = ActivityFormSet(
                instance=self.transmission
            )
            self.extra_context["feeding_bttle_form"] = FeedingBottleFormSet(
                instance=self.transmission
            )
            self.extra_context["medical_form"] = MedicalEventFormSet(
                instance=self.transmission
            )
            return self.render_to_response(self.get_context_data())
        else:
            raise PermissionDenied

    def form_invalid(self, formset):
        """
        If the form is invalid, render the invalid form.
        redefinition to include ext_context
        """
        self.extra_context["message"] = (
            "La modification de la donnée "
            + formset[0][1]
            + " n'a pas été effectuée merci de vérifier les erreurs"
        )
        self.extra_context[formset[0][0]] = formset[1]
        self.initial = {
            "child": self.transmission.child,
            "comment": self.transmission.comment,
        }
        form = self.form_class(initial=self.initial)
        self.extra_context["form"] = form
        return self.render_to_response(self.get_context_data())

    def get_formset(self, post_data, user):
        """
        takes a request post data, returns a
        list [form_name, verbose_name], form or formset]
        """
        formdict = {
            "sleep_set-TOTAL_FORMS": [
                ["sleep_form", "Sieste"],
                SleepFormSet(post_data, instance=self.transmission),
            ],
            "meal_set-TOTAL_FORMS": [
                ["meal_form", "Repas"],
                MealFormSet(post_data, instance=self.transmission),
            ],
            "activity_set-TOTAL_FORMS": [
                ["activity_form", "Activités"],
                ActivityFormSet(post_data, instance=self.transmission),
            ],
            "feedingbottle_set-TOTAL_FORMS": [
                ["feeding_bttle_form", "Biberons"],
                FeedingBottleFormSet(post_data, instance=self.transmission),
            ],
            "medicalevent_set-TOTAL_FORMS": [
                ["medical_form", "Médical"],
                MedicalEventFormSet(post_data, instance=self.transmission),
            ],
        }
        form_name = ["form", "Commentaire"]
        form = self.form_class(
            data={
                "child": self.transmission.child,
                "employee": user,
                "comment": post_data.get("comment"),
            }
        )
        for key, data in formdict.items():
            if post_data.get(key):
                form_name = data[0]
                form = data[1]
        return [form_name, form]

    def post(self, request, *args, **kwargs):
        user = get_permission(instance=self, request=request)
        self.transmission = DailyFact.objects.get(pk=kwargs.get("pk"))
        self.initial = {
            "child": self.transmission.child,
            "comment": self.transmission.comment,
        }
        self.extra_context["trans"] = self.transmission
        self.extra_context["sleep_form"] = SleepFormSet(
            instance=self.transmission
        )
        self.extra_context["meal_form"] = MealFormSet(
            instance=self.transmission
        )
        self.extra_context["activity_form"] = ActivityFormSet(
            instance=self.transmission
        )
        self.extra_context["feeding_bttle_form"] = FeedingBottleFormSet(
            instance=self.transmission
        )
        self.extra_context["medical_form"] = MedicalEventFormSet(
            instance=self.transmission
        )
        self.success_url = str(self.transmission.pk)
        # checking if the user is the author of dailifact
        # (modification only allowed by author)
        if self.transmission.employee == user:
            formset = self.get_formset(request.POST, user)
            if formset[1].is_valid() and formset[0][0] == "form":
                self.transmission.comment = formset[1].cleaned_data["comment"]
                self.transmission.save()
                self.extra_context["success"] = True
                self.transmission = DailyFact.objects.get(
                    pk=self.transmission.pk
                )
                return self.form_valid(self.form_class())
            elif formset[1].is_valid():
                formset[1].save()
                self.extra_context["success"] = True
                return self.form_valid(self.form_class())
            else:
                self.extra_context["success"] = False
                return self.form_invalid(formset)
        else:
            raise PermissionDenied


class ParentView(LoginRequiredMixin, TemplateView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    template_name = "day_to_day/_parent_trans_list.html"
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context = {"child_care_facility": child_care_facility}
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        try:
            user = FamilyMember.objects.get(username=request.user.username)
            childs = Child.objects.filter(relative=user)
            if user.has_daylyfact_access:
                return self.render_to_response(self.get_context_data())
                self.extra_context["parent"] = user
                self.extra_context["childs"] = childs
        except ObjectDoesNotExist:
            if request.user.is_superuser:
                self.extra_context["parent"] = None
                self.extra_context["childs"] = None
                return self.render_to_response(self.get_context_data())
            raise PermissionDenied


class Child_transmissions_report(LoginRequiredMixin, ListView):
    login_url = "/auth/login/"
    redirect_field_name = "redirect_to"
    model = DailyFact
    template_name = "day_to_day/_parent_child_trans_list.html"

    def get(self, request, *args, **kwargs):
        try:
            child_care_facility = Child_care_facility.objects.get(
                name=settings.STRUCTURE
            )
            self.extra_context = {"child_care_facility": child_care_facility}
        except ObjectDoesNotExist:
            self.extra_context = {"child_care_facility": None}
        try:
            user = FamilyMember.objects.get(username=request.user.username)
            if user.has_daylyfact_access:
                pass
            else:
                raise PermissionDenied
        except ObjectDoesNotExist:
            if request.user.is_superuser:
                pass
            else:
                raise PermissionDenied
        self.object_list = (
            self.get_queryset()
            .filter(child=self.kwargs.get("pk"))
            .order_by("-time_stamp")
        )
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        self.extra_context["child"] = Child.objects.get(
            pk=self.kwargs.get("pk")
        )
        context = self.get_context_data()
        return self.render_to_response(context)
