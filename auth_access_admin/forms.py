"""
forms declaration for auth_admin_access application
"""

from django import forms
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (AuthenticationForm, SetPasswordForm,
                                       UserCreationForm, UsernameField)
from django.utils.translation import gettext_lazy as _

from frontpage.models import New, Child_care_facility
from day_to_day.models import DailyFact

from .models import Employee, FamilyMember


class Login(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': "form-control form-control-user",
               'placeholder': "Entrez Votre Adresse Email",
               }
    )
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password',
                   'class': "form-control form-control-user",
                   'placeholder': "Entrez Votre Mot de Passe",
                   }
        ),
    )


class Password_reset_form(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': "form-control form-control-user",
        }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': "form-control form-control-user",
        }
        ),
    )


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
        user.cc_facility = Child_care_facility.objects.get(
            name=settings.STRUCTURE,
            )
        # automatic setting of employee nr
        last_employee = Employee.objects.order_by(
            "employee_nr").last()
        if last_employee is not None:
            user.employee_nr = last_employee.employee_nr+1
        else:
            user.employee_nr = 1
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


class NewForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = New
        widgets = {
            "content": forms.Textarea(attrs={
                "cols": 40, "rows": 5,
                "class": "form-control form-control-user",
                "placeholder": "Votre Texte"
            }),
        }


class DailyFactForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = DailyFact
        widgets = {
            'comment': forms.Textarea(attrs={
                'cols': 40, 'rows': 5,
                'class': "form-control form-control-user",
                "placeholder": "Votre commentaire"
            }),
        }
