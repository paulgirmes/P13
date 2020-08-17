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
        "auth_access_admin.Address", on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = "Membre Famille"
        verbose_name_plural = "Membres Famille"
    
    def __str__(self):
        return self.first_name+" "+self.last_name


class Employee(User):
    phone = models.CharField("Téléphone d'urgence", max_length=14)
    IdScan = models.ImageField("Pièce d'identité", upload_to="ids")
    address = models.ForeignKey(
        "auth_access_admin.Address", on_delete=models.CASCADE
        )
    occupation = models.CharField("Métier", max_length=100)
    employee_nr = models.PositiveSmallIntegerField(
        "Numéro d'employé", primary_key=True,
        )
    diploma = models.CharField("Plus haut diplôme obtenu", max_length=100)
    Is_manager = models.BooleanField("Direction")
    employee_contract = models.ImageField(
        "Scanner du contrat de travail", upload_to="e_contracts"
        )
    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"

    def __str__(self):
        return self.first_name+" "+self.last_name


class Address(models.Model):
    place_type = models.CharField("Type de voie", max_length=20)
    number = models.PositiveIntegerField("Numéro", blank=True)
    place_name = models.CharField("nom de voie", max_length=100)
    city_name = models.CharField("Ville", max_length=100)
    postal_code = models.PositiveIntegerField("Code postal")
    remarks = models.CharField("Compléments", max_length=200)

    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adresses"

    def __str__(self):
        return "{1}, {2} {3}, {4} {5}".format(self.number, self.place_type, self.place_name, self.postal_code, self.city_name)


    #helper to pas the address formatteds to the template for GoogleMapAPI
    def gg_adress_format(self):
        return quote(str(self.number))+\
            "+"+quote(str(self.place_type))+\
            "+"+quote(str(self.place_name))+\
            "+"+quote(str(self.city_name))+"+"+quote((str(self.postal_code)))