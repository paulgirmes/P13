from django.contrib import admin
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
from day_to_day.models import Child, Family_link
from .forms import Login

class ChildCareAdmin(admin.AdminSite):
    child_care_facility = Child_care_facility.objects.get(name__icontains=settings.STRUCTURE)
    app_index_template = "admin/auth_access_admin/admin/admin/admin/app_index.html"
    index_template = "admin/auth_access_admin/admin/admin/admin/index.html"
    password_change_template= "admin/auth_access_admin/admin/admin/admin/user/change_password.html"
    site_header = "administration de la structure"
    site_title = "administration"
    login_template = "auth_access_admin/admin/admin/admin/_login.html"
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



class EmployeeCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + (
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
            "phone",
            "IdScan",
            "address",
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
            'fields': ('username', 'password1', 'password2',
            "phone",
            "IdScan",
            "address",
            ),
        }),
    )
    fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'password', "phone",
                    "IdScan",
                    "address",
                    ),
            }),
        )


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
            'fields': ('username', 'password1', 'password2', "phone",
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
            'fields': ('username', 'password', "phone",
                "IdScan",
                "address",
                "occupation",
                "diploma",
                "Is_manager",
                "employee_contract",),
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

class FamilyLinkInline(admin.TabularInline):
    model = Family_link
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/tabular.html"

class ChildAdmin(NewAdmin):
        inlines = (FamilyLinkInline,)

admin_site.register(New, NewAdmin)
admin_site.register(FamilyMember, FamilyUserAdmin)
admin_site.register(Employee, EmployeeUserAdmin)
admin_site.register(Address)
admin_site.register(Child, ChildAdmin)

