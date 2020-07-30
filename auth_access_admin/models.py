"""
Models regarding user access
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from frontpage.models import User


class FamilyMember(User):
    phone = models.CharField(_("Emergency Contact Phone Number"), max_length=14)
    IdScan = models.ImageField(_("Scan of Employee ID"), upload_to="ids")


class Employee(FamilyMember):
    occupation = models.CharField(_("Employee Job Type"), max_length=100)
    employee_nr = models.PositiveSmallIntegerField(_("Em)ployee Number"), primary_key=True)
    diploma = models.CharField(_("Highest Field Diploma obtained"), max_length=100)
    Is_manager = models.BooleanField(_("Manager of the CC facility"))
    employee_contract = models.ImageField(_("Scan of Employee's Work Contract"), upload_to="e_contracts")


class Address(models.Model):
    place_type = models.CharField(_("Place Descriptor (Road, Way, drive...)"), max_length=20)
    number = models.PositiveIntegerField(_("Number"), blank=True)
    place_name = models.CharField(_("Name of the place"), max_length=100)
    city_name = models.CharField(_("City Name"), max_length=100)
    postal_code = models.PositiveIntegerField(_("Postal Code"))
    remarks = models.CharField(_("Anything Else !"), max_length=200)