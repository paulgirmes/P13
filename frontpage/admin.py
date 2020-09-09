from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Child_care_facility, New
from auth_access_admin.models import FamilyMember, Employee, Address
from day_to_day.models import (
    EmployeeScheduledDay,
    Child,
    OpenDay,
    Family_link,
    DailyFact,
    Sleep,
    Meal,
    FeedingBottle,
    Activity,
    MedicalEvent,
)
from django.contrib.auth.forms import (
    UserCreationForm,
)


class AdvancedAdmin(admin.AdminSite):
    pass


advanced_admin = AdvancedAdmin()


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "phone",
            "IdScan",
            "address",
        )


class FamilyCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = FamilyMember
        fields = UserCreationForm.Meta.fields + (
            "phone",
            "IdScan",
            "address",
            "has_daylyfact_access",
        )


class FamilyUserAdmin(UserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
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


class EmployeeUserAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "phone",
                    "IdScan",
                    "address",
                    "occupation",
                    "employee_nr",
                    "diploma",
                    "Is_manager",
                    "employee_contract",
                ),
            },
        ),
    )


advanced_admin.register(User, UserAdmin)
advanced_admin.register(Child_care_facility)
advanced_admin.register(New)
advanced_admin.register(FamilyMember, FamilyUserAdmin)
advanced_admin.register(Employee, EmployeeUserAdmin)
advanced_admin.register(Address)
advanced_admin.register(Child)
advanced_admin.register(OpenDay)
advanced_admin.register(EmployeeScheduledDay)
advanced_admin.register(Family_link)
advanced_admin.register(DailyFact)
advanced_admin.register(Sleep)
advanced_admin.register(Meal)
advanced_admin.register(FeedingBottle)
advanced_admin.register(Activity)
advanced_admin.register(MedicalEvent)
