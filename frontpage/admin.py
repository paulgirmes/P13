from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Child_care_facility, New
from auth_access_admin.models import FamilyMember, Employee, Address


admin.site.register(User, UserAdmin)
admin.site.register(Child_care_facility)
admin.site.register(New)
admin.site.register(FamilyMember)
admin.site.register(Employee)
admin.site.register(Address)