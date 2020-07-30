from django import forms
from django.contrib.auth.forms import AuthenticationForm


class Login(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control form-control-user"
        self.fields['username'].widget.attrs['placeholder'] = "Entrer Votre Adresse Mail..."
        self.fields["password"].widget.attrs['placeholder'] = "Votre Mot de Passe"
