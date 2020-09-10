"""
Models regarding user access
"""

from django.db import models

from frontpage.models import User
from urllib.parse import quote


class FamilyMember(User):
    phone = models.CharField("Téléphone d'urgence", max_length=14)
    IdScan = models.ImageField("Pièce d'identité", upload_to="ids")
    address = models.ForeignKey(
        "auth_access_admin.Address",
        on_delete=models.CASCADE,
        verbose_name="Adresse",
    )
    has_daylyfact_access = models.BooleanField(
        "Accès aux transmissions",
        default=False,
    )

    class Meta:
        verbose_name = "Membre Familial"
        verbose_name_plural = "Membres de la Famille"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Employee(User):
    phone = models.CharField("Téléphone d'urgence", max_length=14)
    IdScan = models.ImageField("Pièce d'identité", upload_to="ids")
    address = models.ForeignKey(
        "auth_access_admin.Address",
        on_delete=models.CASCADE,
        verbose_name="Adresse",
    )
    cc_facility = models.ForeignKey(
        "frontpage.Child_care_facility",
        on_delete=models.CASCADE,
        verbose_name="Structure",
    )
    occupation = models.CharField("Métier", max_length=100)
    employee_nr = models.PositiveSmallIntegerField(
        "Numéro d'employé",
        primary_key=True,
    )
    diploma = models.CharField("Plus haut diplôme obtenu", max_length=100)
    Is_manager = models.BooleanField("Direction")
    employee_contract = models.ImageField(
        "Scanner du contrat de travail", upload_to="e_contracts"
    )

    class Meta:
        verbose_name = "Salarié"
        verbose_name_plural = "Salariés"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Address(models.Model):
    place_type = models.CharField("Type de voie", max_length=20)
    number = models.PositiveIntegerField("Numéro", blank=True)
    place_name = models.CharField("nom de voie", max_length=100)
    city_name = models.CharField("Ville", max_length=100)
    postal_code = models.PositiveIntegerField("Code postal")
    remarks = models.CharField(
        "Compléments",
        blank=True,
        max_length=200,
    )

    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adresses"

    def __str__(self):
        return "{}, {} {}, {} {}".format(
            self.number,
            self.place_type,
            self.place_name,
            self.postal_code,
            self.city_name,
        )

    # helper to pas the address formatteds to the template for GoogleMapAPI

    def gg_adress_format(self):
        return (
            quote(str(self.number))
            + "+"
            + quote(str(self.place_type))
            + "+"
            + quote(str(self.place_name))
            + "+"
            + quote(str(self.city_name))
            + "+"
            + quote((str(self.postal_code)))
        )
