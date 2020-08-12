from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _


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
