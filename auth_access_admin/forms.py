from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField



class Login(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': "form-control form-control-user",
            'placeholder': "Entrez Votre Adresse Mail",
            }
        )
    )

    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password',
                'class': "form-control form-control-user",
                'placeholder': "EntrezVotre Mot de Passe",
            }
        ),
    )
