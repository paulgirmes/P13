"""
unit tests for auth_access_admin views
"""

from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.test import TestCase, RequestFactory
from frontpage.models import Child_care_facility, User
from auth_access_admin.models import Address, Employee, FamilyMember
from day_to_day.models import Message
from auth_access_admin import views
from auth_access_admin.forms import Password_reset_form


class Login_page(TestCase):
    def test_login_page_exists_access(self):
        request = RequestFactory().get("auth/login/")
        view = views.Login_page()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_login_page_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("auth:login"))
        view = views.Login_page()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_login_page_uses_correct_template(self):
        request = RequestFactory().get(reverse("auth:login"))
        view = views.Login_page()
        view.setup(request)
        self.assertEqual(view.template_name, "auth_access_admin/_login.html")


class Reset_PasswordTest(TestCase):
    def test_reset_Password_page_exists_access(self):
        request = RequestFactory().get("accounts/password_reset/")
        view = views.Reset_Password()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_reset_Password_page_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("auth:password_reset"))
        view = views.Reset_Password()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_reset_Password_page_uses_correct_template(self):
        request = RequestFactory().get(reverse("auth:password_reset"))
        view = views.Reset_Password()
        view.setup(request)
        self.assertEqual(
            view.template_name, "auth_access_admin/_forgot-password.html"
        )
        self.assertEqual(view.success_url, reverse("auth:password_reset_done"))


class PasswordResetDoneViewTest(TestCase):
    def test_password_reset_done_page_exists(self):
        request = RequestFactory().get("accounts/password_reset/done/")
        view = views.PasswordResetDoneView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_password_reset_done_page_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("auth:password_reset_done"))
        view = views.PasswordResetDoneView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_password_reset_done_page_uses_correct_template(self):
        request = RequestFactory().get(reverse("auth:password_reset_done"))
        view = views.PasswordResetDoneView()
        view.setup(request)
        self.assertEqual(
            view.template_name, "auth_access_admin/_password_reset_done.html"
        )


class PasswordResetConfirmViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "superuser@hotmail.com",
            first_name="prénom",
            last_name="Nom",
            password="123456789879/",
            email="nomprenom@hotmail.com",
            is_superuser=True,
        )

    def test_password_reset_confirm_page_uses_correct_template(self):
        view = views.PasswordResetConfirmView()
        self.assertEqual(
            view.template_name,
            "auth_access_admin/_password_reset_confirm.html",
        )
        self.assertEqual(view.form_class, Password_reset_form)
        self.assertEqual(
            view.success_url, reverse("auth:password_reset_complete")
        )


class PasswordResetCompleteViewTest(TestCase):
    def test_password_reset_confirm_view_page_exists(self):
        request = RequestFactory().get("account/password_reset_complete/")
        view = views.PasswordResetCompleteView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_password_reset_confirm_page_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("auth:password_reset_complete"))
        view = views.PasswordResetCompleteView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_password_reset_confirm_page_uses_correct_template(self):
        request = RequestFactory().get(reverse("auth:password_reset_complete"))
        view = views.PasswordResetCompleteView()
        view.setup(request)
        self.assertEqual(
            view.template_name,
            "auth_access_admin/_password_reset_complete.html",
        )


class Index(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "superuser@hotmail.com",
            first_name="prénom",
            last_name="Nom",
            password="123456789879/",
            email="nomprenom@hotmail.com",
            is_superuser=True,
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
        cls.message = Message.objects.create(
            cc_facility=cls.cc_facility, title="title", content="content"
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
            address=cls.address,
            cc_facility=cls.cc_facility,
        )
        cls.employee_not_manager = Employee.objects.create_user(
            first_name="prénom",
            last_name="Nom",
            password="123456789",
            username="employee_no_access@hotmail.com",
            phone=13510006788,
            IdScan="/fakepath/jfoijhzefe.jpg",
            occupation="healthcare",
            employee_nr="145",
            diploma="CPA",
            Is_manager=False,
            employee_contract="/fakepath/jfoijhzefe.jpg",
            address=cls.address,
            cc_facility=cls.cc_facility,
        )
        cls.family_member = FamilyMember.objects.create_user(
            first_name="prénom",
            last_name="Nom",
            password="123456789",
            username="family@hotmail.com",
            phone=13510006788,
            IdScan="/fakepath/jfoijhzefe.jpg",
            has_daylyfact_access=True,
            address=cls.address,
        )

        cls.family_member_no_access = FamilyMember.objects.create_user(
            first_name="prénom2",
            last_name="Nom2",
            password="123456789",
            username="family2@hotmail.com",
            phone=13510006788,
            IdScan="/fakepath/jfoijhzefe.jpg",
            has_daylyfact_access=False,
            address=cls.address,
        )

    def test_index_page_exist(self):
        request = RequestFactory().get("auth/index/")
        request.user = self.employee
        view = views.Index()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_index_page_access_denied(self):
        response = self.client.get(reverse("auth:index"))
        self.assertEqual(response.status_code, 302)

    def test_index_page_exists_access_manager_allowed(self):
        request = RequestFactory().get("auth:index")
        request.user = self.employee
        view = views.Index()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_index_page_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("auth:index"))
        request.user = self.employee
        view = views.Index()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_index_page_uses_correct_template(self):
        request = RequestFactory().get(reverse("auth:index"))
        request.user = self.employee
        view = views.Index()
        view.setup(request)
        self.assertEqual(view.template_name, "auth_access_admin/_index.html")

    def test_permission_denied_familly_no_access(self):
        with self.assertRaises(PermissionDenied):
            request = RequestFactory().get(reverse("auth:index"))
            request.user = self.family_member_no_access
            view = views.Index()
            view.setup(request)
            view.get(request)

    def test_index_page_exists_access_superuser_allowed(self):
        request = RequestFactory().get(reverse("auth:index"))
        request.user = self.user
        view = views.Index()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_context_exists_manager(self):
        request = RequestFactory().get(reverse("auth:index"))
        request.user = self.employee
        view = views.Index()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(
            view.extra_context.get("employee").username, self.employee.username
        )
        self.assertEqual(view.extra_context.get("child_number"), 0)
        self.assertEqual(view.extra_context.get("events_today"), 0)
        self.assertEqual(view.extra_context.get("medical_event_today"), 0)
        self.assertEqual(view.extra_context.get("fill_ratio"), 0)

    def test_context_exists_superuser(self):
        request = RequestFactory().get(reverse("auth:index"))
        request.user = self.user
        view = views.Index()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"),
            self.cc_facility,
        )
        self.assertEqual(
            view.extra_context.get("employee").username, self.user.username
        )

    def test_redirects_non_manager_employee(self):
        self.assertTrue(
            self.client.login(
                username="employee_no_access@hotmail.com", password="123456789"
            )
        )
        response = self.client.get(reverse("auth:index"))
        self.assertRedirects(response, expected_url="/day-to-day/employe/")
        self.client.logout()

    def test_redirects_family_has_access(self):
        self.assertTrue(
            self.client.login(
                username="family@hotmail.com", password="123456789"
            )
        )
        response = self.client.get(reverse("auth:index"))
        self.assertRedirects(response, expected_url="/day-to-day/parent/")


class LogoutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "superuser@hotmail.com",
            first_name="prénom",
            last_name="Nom",
            password="123456789879/",
            email="nomprenom@hotmail.com",
            is_superuser=True,
        )

    def test_index_page_exists(self):
        self.assertTrue(
            self.client.login(
                username="superuser@hotmail.com", password="123456789879/"
            )
        )
        response = self.client.get("/auth/logout/")
        self.assertEqual(response.status_code, 302)

    def test_index_page_url_accessible_by_name(self):
        response = self.client.get(reverse("auth:logout"))
        self.assertEqual(response.status_code, 302)
