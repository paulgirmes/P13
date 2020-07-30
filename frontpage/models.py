from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# custom user model
class User(AbstractUser):
    username = models.EmailField(
    _('email address'),
    unique=True,
    error_messages={
        'unique': _("A user with that username already exists."),
    },
    )