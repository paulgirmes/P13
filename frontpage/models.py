from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


# custom user model


class User(AbstractUser):
    first_name = models.CharField(
        _("first name"),
        max_length=30,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
    )
    username = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    EMAIL_FIELD = "username"

    def __str__(self):
        return self.username


class Child_care_facility(models.Model):
    name = models.CharField("Nom de la structure", max_length=50, unique=True)
    max_child_number = models.IntegerField(
        "Places maximum",
    )
    type_of_facility = models.CharField(
        "Type de structure",
        max_length=50,
        choices=[
            ("MC", "Micro-Crèche"),
            ("C", "Crèche"),
            ("MAM", "MAM"),
            ("MC", "Crèche-Parentale"),
            ("MC", "Crèche-Municipale"),
            ("MC", "Crèche d'entreprise"),
            ("MC", "Crèche associative"),
        ],
    )
    status = models.CharField(
        "Statut",
        max_length=50,
        choices=[
            ("A", "Active"),
            ("NA", "Non Active"),
            ("EC", "En cours de création"),
        ],
    )
    address = models.ForeignKey(
        "auth_access_admin.Address",
        on_delete=models.CASCADE,
        verbose_name="Adresse",
    )
    phone = models.CharField("Téléphone", max_length=14)
    email = models.EmailField("Adresse Email")

    class Meta:
        verbose_name = "Structure de Garde"
        verbose_name_plural = "Structures de Garde"

    def __str__(self):
        return self.name


class New(models.Model):
    date_time = models.DateTimeField(
        "Horodatage",
        auto_now_add=True,
    )
    title = models.CharField(
        "Titre",
        max_length=50,
    )
    content = models.CharField(
        "Contenu texte",
        max_length=200,
        blank=True,
    )
    img_url = models.ImageField("image", upload_to="news_img")
    cc_facility = models.ForeignKey(
        Child_care_facility,
        on_delete=models.CASCADE,
        verbose_name="Structure de Garde",
    )

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
