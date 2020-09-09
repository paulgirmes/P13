"""
unit tests for auth_access_admin models
"""

from django.test import TestCase
from auth_access_admin.models import Address, FamilyMember, Employee


class FamilyMember_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            place_type="rue",
            number=12,
            place_name="bellevue",
            city_name="toulouse",
            postal_code=31300,
        )
        cls.family_member = FamilyMember.objects.create(
            first_name="prénom",
            last_name="Nom",
            password="123456789",
            username="nomprenom@hotmail.com",
            phone=13510006788,
            IdScan="/fakepath/jfoijhzefe.jpg",
            has_daylyfact_access=True,
            address=cls.address,
        )

    def test_str(self):
        self.assertEqual(str(self.family_member), "prénom Nom")

    def test_phone_label(self):
        field_label = self.family_member._meta.get_field("phone").verbose_name
        self.assertEqual(field_label, "Téléphone d'urgence")

    def test_IdScan_label(self):
        field_label = self.family_member._meta.get_field("IdScan").verbose_name
        self.assertEqual(field_label, "Pièce d'identité")

    def test_address_label(self):
        field_label = self.family_member._meta.get_field(
            "address").verbose_name
        self.assertEqual(field_label, "Adresse")

    def test_has_daylyfact_access_label(self):
        field_label = self.family_member._meta.get_field(
            "has_daylyfact_access").verbose_name
        self.assertEqual(field_label, "Accès aux transmissions")


class Employee_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            place_type="rue",
            number=12,
            place_name="bellevue",
            city_name="toulouse",
            postal_code=31300,
        )
        cls.employee = Employee.objects.create_user(
            first_name="prénom",
            last_name="Nom",
            password="123456789",
            username="employe@hotmail.com",
            phone=13510006788,
            IdScan="/fakepath/jfoijhzefe.jpg",
            occupation="healthcare",
            employee_nr="12313",
            diploma="CPA",
            Is_manager=True,
            employee_contract="/fakepath/jfoijhzefe.jpg",
            address=cls.address
        )

    def test_str(self):
        self.assertEqual(str(self.employee), "prénom Nom")

    def test_phone_label(self):
        field_label = self.employee._meta.get_field("phone").verbose_name
        self.assertEqual(field_label, "Téléphone d'urgence")

    def test_IdScan_label(self):
        field_label = self.employee._meta.get_field("IdScan").verbose_name
        self.assertEqual(field_label, "Pièce d'identité")

    def test_address_label(self):
        field_label = self.employee._meta.get_field("address").verbose_name
        self.assertEqual(field_label, "Adresse")

    def test_occupation_label(self):
        field_label = self.employee._meta.get_field("occupation").verbose_name
        self.assertEqual(field_label, "Métier")

    def test_employee_nr_label(self):
        field_label = self.employee._meta.get_field("employee_nr").verbose_name
        self.assertEqual(field_label, "Numéro d'employé")

    def test_diploma_label(self):
        field_label = self.employee._meta.get_field("diploma").verbose_name
        self.assertEqual(field_label, "Plus haut diplôme obtenu")

    def test_Is_manager_label(self):
        field_label = self.employee._meta.get_field("Is_manager").verbose_name
        self.assertEqual(field_label, "Direction")

    def test_employee_contract_label(self):
        field_label = self.employee._meta.get_field(
            "employee_contract").verbose_name
        self.assertEqual(field_label, "Scanner du contrat de travail")


class Address_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            place_type="rue",
            number=12,
            place_name="bellevue",
            city_name="toulouse",
            postal_code=31300,
        )

    def test_str(self):
        self.assertEqual(str(self.address), "12, rue bellevue, 31300 toulouse")

    def test_place_type_label(self):
        field_label = self.address._meta.get_field("place_type").verbose_name
        self.assertEqual(field_label, "Type de voie")

    def test_number_label(self):
        field_label = self.address._meta.get_field("number").verbose_name
        self.assertEqual(field_label, "Numéro")

    def test_place_name_label(self):
        field_label = self.address._meta.get_field("place_name").verbose_name
        self.assertEqual(field_label, "nom de voie")

    def test_city_name_label(self):
        field_label = self.address._meta.get_field("city_name").verbose_name
        self.assertEqual(field_label, "Ville")

    def test_postal_code_label(self):
        field_label = self.address._meta.get_field("postal_code").verbose_name
        self.assertEqual(field_label, "Code postal")

    def test_remarks_label(self):
        field_label = self.address._meta.get_field("remarks").verbose_name
        self.assertEqual(field_label, "Compléments")

    def test_gg_adress_format(self):
        formatted_address = Address.gg_adress_format(self.address)
        self.assertEqual(formatted_address, "12+rue+bellevue+toulouse+31300")
