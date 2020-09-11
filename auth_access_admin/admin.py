"""
Custom basic admin-site for Child care Structure
and web-page management.
"""

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.contrib.admin import ModelAdmin
from frontpage.models import New, Child_care_facility
from .models import FamilyMember, Employee, Address
from day_to_day.models import (
    Child,
    Family_link,
    DailyFact,
    Sleep,
    Meal,
    FeedingBottle,
    Activity,
    MedicalEvent,
    Message,
)
from .forms import (
    Login,
    EmployeeCreationForm,
    FamilyCreationForm,
    NewForm,
    DailyFactForm,
)


class ChildCareAdmin(admin.AdminSite):
    """
    Child Care minimal admin site class
    """
    try:
        child_care_facility = Child_care_facility.objects.get(
            name=settings.STRUCTURE
        )
    except ObjectDoesNotExist:
        child_care_facility = None
    app_index_template = (
        "admin/auth_access_admin/admin/app_index.html"
    )
    index_template = "admin/auth_access_admin/admin/index.html"
    password_change_template = (
        "admin/auth_access_admin/admin/user/change_password.html"
    )
    site_header = "administration de la structure"
    site_title = "administration"
    login_template = "auth_access_admin/_login.html"
    login_form = Login

    # adds custom context for each request
    def each_context(self, request):
        context = super().each_context(request)
        if request.user.username:
            try:
                employee = Employee.objects.get(
                    username__contains=request.user.username
                )
                context.update({"employee": employee})
            except ObjectDoesNotExist:
                context.update({"employee": request.user})
        context.update({"child_care_facility": self.child_care_facility})
        return context


admin_site = ChildCareAdmin(name="structure_admin")


class FamilyLinkInline(admin.TabularInline):
    model = Family_link
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/stacked.html"


class SleepInline(admin.TabularInline):
    model = Sleep
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/stacked.html"


class MealInline(admin.TabularInline):
    model = Meal
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/stacked.html"


class FeedingBottleInline(admin.TabularInline):
    model = FeedingBottle
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/stacked.html"


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/stacked.html"


class MedicalEventInline(admin.TabularInline):
    model = MedicalEvent
    extra = 1
    template = "admin/auth_access_admin/admin//edit_inline/stacked.html"


class FamilyUserAdmin(UserAdmin):
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_list_template = "admin/auth_access_admin/admin/change_list.html"
    delete_confirmation_template = (
        "admin/auth_access_admin/admin/delete_confirmation.html"
    )
    delete_selected_confirmation_template = (
        "admin/auth_access_admin/admin/delete_selected_confirmation.html"
    )
    object_history_template = (
        "admin/auth_access_admin/admin/object_history.html"
    )
    popup_response_template = (
        "admin/auth_access_admin/admin/popup_response.html"
    )
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_user_password_template = (
        "admin/auth_access_admin/admin/user/change_password.html"
    )
    add_form = FamilyCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password1",
                    "password2",
                    "phone",
                    "IdScan",
                    "address",
                    "has_daylyfact_access",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password",
                    "phone",
                    "IdScan",
                    "address",
                    "has_daylyfact_access",
                ),
            },
        ),
    )
    inlines = [
        FamilyLinkInline,
    ]


class EmployeeUserAdmin(UserAdmin):
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_list_template = "admin/auth_access_admin/admin/change_list.html"
    delete_confirmation_template = (
        "admin/auth_access_admin/admin/delete_confirmation.html"
    )
    delete_selected_confirmation_template = (
        "admin/auth_access_admin/admin/delete_selected_confirmation.html"
    )
    object_history_template = (
        "admin/auth_access_admin/admin/object_history.html"
    )
    popup_response_template = (
        "admin/auth_access_admin/admin/popup_response.html"
    )
    change_user_password_template = (
        "admin/auth_access_admin/admin/user/change_password.html"
    )
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    add_form = EmployeeCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password1",
                    "password2",
                    "phone",
                    "IdScan",
                    "address",
                    "occupation",
                    "diploma",
                    "Is_manager",
                    "employee_contract",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password",
                    "phone",
                    "IdScan",
                    "address",
                    "occupation",
                    "diploma",
                    "Is_manager",
                    "employee_contract",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.cc_facility = Child_care_facility.objects.get(
            name=settings.STRUCTURE
        )
        super().save_model(request, obj, form, change)


class CustomModelAdmin(ModelAdmin):
    add_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_form_template = "admin/auth_access_admin/admin/change_form.html"
    change_list_template = "admin/auth_access_admin/admin/change_list.html"
    delete_confirmation_template = (
        "admin/auth_access_admin/admin/delete_confirmation.html"
    )
    delete_selected_confirmation_template = (
        "admin/auth_access_admin/admin/delete_selected_confirmation.html"
    )
    object_history_template = (
        "admin/auth_access_admin/admin/object_history.html"
    )
    popup_response_template = (
        "admin/auth_access_admin/admin/popup_response.html"
    )
    exclude = ("cc_facility",)

    def save_model(self, request, obj, form, change):
        obj.cc_facility = Child_care_facility.objects.get(
            name=settings.STRUCTURE
        )
        super().save_model(request, obj, form, change)


class NewAdmin(CustomModelAdmin):
    form = NewForm
    pass


class MessageAdmin(CustomModelAdmin):
    pass


class AdressAdmin(CustomModelAdmin):
    pass


class ChildAdmin(CustomModelAdmin):
    inlines = [
        FamilyLinkInline,
    ]


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
