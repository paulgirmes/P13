"""
forms declaration for auth_admin_access application
"""
import datetime
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


class ChildForm(forms.ModelForm):
    def _post_clean(self):
        """
        Sanity checks for birthdate and vaccine
        """
        if self.cleaned_data["birth_date"] > datetime.datetime.now().date():
            self.add_error(
                "birth_date",
                ["Veuillez renseigner une date antérieure à aujourd'hui."],
                )
        if self.cleaned_data[
                "vaccine_next_due_date"
                ] < datetime.datetime.now().date():
            self.add_error(
                "vaccine_next_due_date",
                ["Veuillez renseigner une date postérieure à aujourd'hui."],
                )
        super()._post_clean()


class MedicalEventForm(forms.ModelForm):
    def _post_clean(self):
        """
        Sanity checks for Paracetamol admin time
        """
        if self.cleaned_data.get(
            "paracetamol_given_time"
            ) is None and self.cleaned_data.get(
                "given_paracetamol_qtty_mg"):
            self.add_error(
                "paracetamol_given_time",
                ["Veuillez renseigner une heure."]
                )

        if self.cleaned_data.get("paracetamol_given_time") is not None:
            if self.cleaned_data[
                    "paracetamol_given_time"
                    ] > datetime.datetime.now().time():
                self.add_error(
                    "paracetamol_given_time",
                    ["Veuillez renseigner une heure antérieure à maintenant."],
                    )
        super()._post_clean()


class FeedingBottleForm(forms.ModelForm):
    def _post_clean(self):
        """
        Sanity checks for qtty's
        """
        if self.cleaned_data.get(
                "drank_qtty_ml"
            ) and self.cleaned_data.get(
                    "prepared_qtty_ml"):
            if self.cleaned_data[
                    "drank_qtty_ml"
                    ] > self.cleaned_data["prepared_qtty_ml"]:
                self.add_error(
                    "drank_qtty_ml",
                    [
                        "La quantité bue ne peut être supérieure à celle "
                        + "préparée."
                    ],
                    )
        super()._post_clean()
