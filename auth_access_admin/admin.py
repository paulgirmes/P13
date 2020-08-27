from django.contrib import admin
from django.forms import ModelForm, Textarea
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.admin import ModelAdmin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, UsernameField
)
from django.views.decorators.cache import never_cache
from frontpage.models import New, Child_care_facility
from .models import FamilyMember, Employee, Address
from day_to_day.models import (Child, OpenDay, EmployeeScheduledDay,
        ChildScheduledDay, Family_link, DailyFact, Sleep, Meal,
        FeedingBottle, Activity, MedicalEvent, Message
        )
from .forms import Login

class ChildCareAdmin(admin.AdminSite):
    child_care_facility = Child_care_facility.objects.get(name__icontains=settings.STRUCTURE)
    app_index_template = "admin/auth_access_admin/admin/admin/admin/app_index.html"
    index_template = "admin/auth_access_admin/admin/admin/admin/index.html"
    password_change_template= "admin/auth_access_admin/admin/admin/admin/user/change_password.html"
    site_header = "administration de la structure"
    site_title = "administration"
    login_template = "auth_access_admin/_login.html"
    login_form = Login

    def each_context(self, request):
        context = super().each_context(request)
        if request.user.username:
            try:
                employee = Employee.objects.get(username__contains=request.user.username)
                context.update(
                {"employee" : employee}
                )
            except:
               context.update(
                {"employee" : request.user}
                )
        context.update(
            {"child_care_facility" : self.child_care_facility}
        )
        return context

admin_site = ChildCareAdmin(name='structure_admin')


class FamilyLinkInline(admin.TabularInline):
    model = Family_link
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/tabular.html"


class SleepInline(admin.TabularInline):
    model = Sleep
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/tabular.html"


class MealInline(admin.TabularInline):
    model = Meal
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/tabular.html"


class FeedingBottleInline(admin.TabularInline):
    model = FeedingBottle
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/tabular.html"


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/tabular.html"


class MedicalEventInline(admin.TabularInline):
    model = MedicalEvent
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/tabular.html"


class EmployeeCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "phone",
            "IdScan",
            "address",
            "occupation",
            "diploma",
            "Is_manager",
            "employee_contract",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.employee_nr = Employee.objects.order_by("employee_nr").last().employee_nr+1
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class FamilyCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = FamilyMember
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "phone",
            "IdScan",
            "address",
            "has_daylyfact_access",
        )

class FamilyUserAdmin(UserAdmin):
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_list_template = "admin/auth_access_admin/admin/change_list.html"
    delete_confirmation_template = "admin/auth_access_admin/admin/delete_confirmation.html"
    delete_selected_confirmation_template = "admin/auth_access_admin/admin/delete_selected_confirmation.html"
    object_history_template = "admin/auth_access_admin/admin/object_history.html"
    popup_response_template = "admin/auth_access_admin/admin/popup_response.html"
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_user_password_template = "admin/auth_access_admin/admin/user/change_password.html"
    add_form = FamilyCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
                'fields': (
                    "first_name",
                    "last_name",
                    'username',
                    'password1',
                    'password2',
                    "phone",
                    "IdScan",
                    "address",
                    "has_daylyfact_access",
                    ),
        }),
    )
    fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': (
                    "first_name",
                    "last_name",
                    'username',
                    'password',
                    "phone",
                    "IdScan",
                    "address",
                    "has_daylyfact_access",
                    ),
            }),
        )
    inlines = [
            FamilyLinkInline,
        ]


class EmployeeUserAdmin(UserAdmin):
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_list_template = "admin/auth_access_admin/admin/change_list.html"
    delete_confirmation_template = "admin/auth_access_admin/admin/delete_confirmation.html"
    delete_selected_confirmation_template = "admin/auth_access_admin/admin/delete_selected_confirmation.html"
    object_history_template = "admin/auth_access_admin/admin/object_history.html"
    popup_response_template = "admin/auth_access_admin/admin/popup_response.html"
    change_user_password_template = "admin/auth_access_admin/admin/user/change_password.html"
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    add_form = EmployeeCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "first_name",
                "last_name",
                'username',
                'password1',
                'password2',
                "phone",
                "IdScan",
                "address",
                "occupation",
                "diploma",
                "Is_manager",
                "employee_contract",),
        }),
    )
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                    "first_name",
                    "last_name",
                    'username',
                    'password',
                    "phone",
                    "IdScan",
                    "address",
                    "occupation",
                    "diploma",
                    "Is_manager",
                    "employee_contract",
                ),
        }),
    )

class CustomModelAdmin(ModelAdmin):
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_list_template = "admin/auth_access_admin/admin/change_list.html"
    delete_confirmation_template = "admin/auth_access_admin/admin/delete_confirmation.html"
    delete_selected_confirmation_template = "admin/auth_access_admin/admin/delete_selected_confirmation.html"
    object_history_template = "admin/auth_access_admin/admin/object_history.html"
    popup_response_template = "admin/auth_access_admin/admin/popup_response.html"


class NewAdmin(CustomModelAdmin):
    exclude =(
        "cc_facility",
    )
    def save_model(self, request, obj, form, change):
        obj.cc_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
        super().save_model(request, obj, form, change)


class MessageAdmin(NewAdmin):
    pass


class AdressAdmin(NewAdmin):
    pass


class ChildAdmin(NewAdmin):
        inlines = [
            FamilyLinkInline,
        ]


class DailyFactForm(ModelForm):
 class Meta:
        widgets = {
            'comment': Textarea(attrs={
                'cols': 40, 'rows': 5,
                'class': "form-control form-control-user",
                "placeholder": "Votre commentaire"
            }),
        }


class DailyFactAdmin(NewAdmin):
    inlines = [
                SleepInline,
                MealInline,
                FeedingBottleInline,
                ActivityInline,
                MedicalEventInline,
            ]
    form = DailyFactForm

admin_site.register(New, NewAdmin)
admin_site.register(FamilyMember, FamilyUserAdmin)
admin_site.register(Employee, EmployeeUserAdmin)
admin_site.register(Address, AdressAdmin)
admin_site.register(Child, ChildAdmin)
admin_site.register(DailyFact, DailyFactAdmin)
admin_site.register(Message, MessageAdmin)

