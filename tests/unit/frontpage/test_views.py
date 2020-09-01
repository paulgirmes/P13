"""
unit tests for frontpage views
"""

from unittest import mock

from django.urls import reverse
from django.test import TestCase, override_settings, RequestFactory
from frontpage.models import New, Child_care_facility, User
from auth_access_admin.models import Address
from frontpage import views

class Page_Not_found_test(TestCase):
    @override_settings(DEBUG=False)
    def test_template(self):
        response = self.client.get("/123/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "frontpage/_404.html")

class Homepage_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "nomprenom@hotmail.com",
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789879/",
            email = "nomprenom@hotmail.com",
        )
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
    def test_homepage_exists(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_accessible_by_name(self):
        response = self.client.get(reverse("frontpage:homepage"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse("frontpage:homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "frontpage/_index.html")

    def test_homepage_nav_header_not_logged_in(self):
        response = self.client.get(reverse("frontpage:homepage"))
        self.assertContains(response, "Connexion")

    def test_homepage_nav_header_logged_in(self):
        self.assertTrue(
            self.client.login(username="nomprenom@hotmail.com", password="123456789879/",)
        )
        response = self.client.get(reverse("frontpage:homepage"))
        self.assertContains(response, "Déconnexion")
        self.client.logout()

    def test_context_exists(self):
        response = self.client.get(reverse("frontpage:homepage"))
        self.assertTrue("news" in response.context)
        self.assertTrue("child_care_facility" in response.context)
        self.assertTrue("gg_adress" in response.context)

    def test_context_isgood(self):
        request = RequestFactory().get(reverse("frontpage:homepage"))
        view = views.HomePage()
        view.setup(request)
        context = view.get_context_data()
        self.assertTrue(context.get("news"), self.new)
        self.assertTrue(context.get("child_care_facility"), self.cc_facility)
        self.assertTrue(context.get("gg_adress"), self.address)


class Legal_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "nomprenom@hotmail.com",
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789879/",
            email = "nomprenom@hotmail.com",
        )
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
    def test_homepage_exists(self):
        response = self.client.get("/conditions-generales/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_accessible_by_name(self):
        response = self.client.get(reverse("frontpage:legal"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse("frontpage:legal"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "frontpage/_legal.html")
    
    def test_context_exists(self):
        response = self.client.get(reverse("frontpage:legal"))
        self.assertTrue("child_care_facility" in response.context)

    def test_context_isgood(self):
        request = RequestFactory().get(reverse("frontpage:legal"))
        view = views.HomePage()
        view.setup(request)
        context = view.get_context_data()
        self.assertTrue(context.get("child_care_facility"), self.cc_facility)
