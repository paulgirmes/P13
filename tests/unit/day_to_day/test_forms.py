"""
unit tests for day_to_day forms
"""

from django.test import TestCase
from frontpage.models import New, Child_care_facility, User
from auth_access_admin.models import Address

class User_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "nomprenom@hotmail.com",
        )
    def test_str(self):
        self.assertEquals(str(self.user), self.user.username)

    def test_username_field(self):
        self.user = User.objects.get(username="nomprenom@hotmail.com")
        email = self.user.get_email_field_name()
        self.assertEquals(email,"username")


class Child_care_facility_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            place_type = "rue",
            number =12,
            place_name = "bellevue",
            city_name = "toulouse",
            postal_code = "31300"
        )
        cls.cc_facility = Child_care_facility.objects.create(
            name = "les Pitchounous",
            max_child_number = "12",
            type_of_facility = "MAM",
            status = "A",
            address = cls.address,
            phone = "013511225588",
            email = "contact@mamlespichounous.fr",
        )

    def test_str(self):
        self.assertEquals(
            str(self.cc_facility),
            self.cc_facility.name,
            )

    def test_name_label(self):
        field_label = self.cc_facility._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "Nom de la structure")

    def test_max_child_number_label(self):
        field_label = self.cc_facility._meta.get_field("max_child_number").verbose_name
        self.assertEquals(field_label, "Places maximum")

    def test_type_of_facility_label(self):
        field_label = self.cc_facility._meta.get_field("type_of_facility").verbose_name
        self.assertEquals(field_label, "Type de structure")

    def test_status_label(self):
        field_label = self.cc_facility._meta.get_field("status").verbose_name
        self.assertEquals(field_label, "Statut")

    def test_address_label(self):
        field_label = self.cc_facility._meta.get_field("address").verbose_name
        self.assertEquals(field_label, "Adresse")

    def test_phone_label(self):
        field_label = self.cc_facility._meta.get_field("phone").verbose_name
        self.assertEquals(field_label, "Téléphone")

    def test_email_label(self):
        field_label = self.cc_facility._meta.get_field("email").verbose_name
        self.assertEquals(field_label, "Adresse Email")

class New_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            place_type = "rue",
            number =12,
            place_name = "bellevue",
            city_name = "toulouse",
            postal_code = "31300"
        )
        cls.cc_facility = Child_care_facility.objects.create(
            name = "les Pitchounous",
            max_child_number = "12",
            type_of_facility = "MAM",
            status = "A",
            address = cls.address,
            phone = "013511225588",
            email = "contact@mamlespichounous.fr",
        )
        cls.new = New.objects.create(
            title = "nouvelle",
            content = "texte",
            img_url = "media/news_img/IMG_20190106_121539.jpg",
            cc_facility = cls.cc_facility,
        )

    def test_str(self):
        self.assertEquals(str(self.new), self.new.title)

    def test_title_label(self):
        field_label = self.new._meta.get_field("title").verbose_name
        self.assertEquals(field_label, "Titre")

    def test_content_label(self):
        field_label = self.new._meta.get_field("content").verbose_name
        self.assertEquals(field_label, "Contenu texte")

    def test_img_url_label(self):
        field_label = self.new._meta.get_field("img_url").verbose_name
        self.assertEquals(field_label, "image")

    def test_cc_facility_label(self):
        field_label = self.new._meta.get_field("cc_facility").verbose_name
        self.assertEquals(field_label, "Structure de Garde")
