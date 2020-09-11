"""
integration tests for frontpage views
"""


from django.urls import reverse
from django.test import TestCase, RequestFactory
from frontpage.models import New, Child_care_facility, User
from auth_access_admin.models import Address
from frontpage import views


class Homepage_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "nomprenom@hotmail.com",
            first_name="prénom",
            last_name="Nom",
            password="123456789879/",
            email="nomprenom@hotmail.com",
        )
        cls.address = Address.objects.create(
            place_type="rue",
            number=12,
            place_name="bellevue",
            city_name="toulouse",
            postal_code="31300",
        )
        cls.cc_facility = Child_care_facility.objects.create(
            name="xyz",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            address=cls.address,
            phone="013511225588",
            email="contact@mamlespichounous.fr",
        )
        cls.new = New.objects.create(
            title="nouvelle",
            content="texte",
            img_url="media/news_img/IMG_20190106_121539.jpg",
            cc_facility=cls.cc_facility,
        )

    def test_context_isgood(self):
        request = RequestFactory().get(reverse("frontpage:homepage"))
        view = views.HomePage()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("gg_adress"),
            "12+rue+bellevue+toulouse+31300",
        )
