from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Child_care_facility, New
from auth_access_admin.models import FamilyMember, Employee, Address
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
)

# class EmployeeCreationForm(UserCreationForm):

#     class Meta(UserCreationForm.Meta):
#         model = Employee
#         fields = UserCreationForm.Meta.fields + (
#             "phone",
#             "IdScan",
#             "address",
#         )

# class FamilyCreationForm(UserCreationForm):

#     class Meta(UserCreationForm.Meta):
#         model = FamilyMember
#         fields = UserCreationForm.Meta.fields + (
#             "phone",
#             "IdScan",
#             "address",
#         )

# class FamilyUserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2',
#             "phone",
#             "IdScan",
#             "address",
#             ),
#         }),
#     )

# class EmployeeUserAdmin(UserAdmin):
#     add_form = EmployeeCreationForm
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', "phone",
#                 "IdScan",
#                 "address",
#                 "occupation",
#                 "employee_nr",
#                 "diploma",
#                 "Is_manager",
#                 "employee_contract",),
#         }),
#     )

# admin.site.register(User, UserAdmin)
# admin.site.register(Child_care_facility)
# admin.site.register(New)
# admin.site.register(FamilyMember, FamilyUserAdmin)
# admin.site.register(Employee, EmployeeUserAdmin)
# admin.site.register(Address)
