from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
)
from frontpage.models import New
from .models import FamilyMember, Employee, Address
from frontpage.models import Child_care_facility
from settings import STRUCTURE


class ChildCareAdmin(AdminSite):
    child_care_facility = Child_care_facility.objects.get(name__icontains=STRUCTURE)
    app_index_template = "admin/auth_access_admin/app_index.html"
    index_template = "admin/auth_access_admin/index.html"
    site_header = "administration de la structure"


    def each_context(self, request):
        context = super().each_context(request)
        try:
            employee = Employee.objects.get(username__contains=request.user.username)
            context.update(
            {"employee" : employee}
            )
        except:
            raise Exception
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
            "employee_nr",
            "diploma",
            "Is_manager",
            "employee_contract",
        )

class FamilyCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = FamilyMember
        fields = UserCreationForm.Meta.fields + (
            "phone",
            "IdScan",
            "address",
        )

class FamilyUserAdmin(UserAdmin):
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
    
    add_form = EmployeeCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', "phone",
                "IdScan",
                "address",
                "occupation",
                "employee_nr",
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
                "employee_nr",
                "diploma",
                "Is_manager",
                "employee_contract",),
        }),
    )

admin_site.register(New)
admin_site.register(FamilyMember, FamilyUserAdmin)
admin_site.register(Employee, EmployeeUserAdmin)
admin_site.register(Address)

