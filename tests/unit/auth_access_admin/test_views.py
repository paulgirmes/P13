"""
unit tests for day_to_day views
"""

from unittest import mock

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from frontpage.models import Child_care_facility, User
from auth_access_admin.models import Address, Employee, FamilyMember
from day_to_day.models import Message, Child, DailyFact, Sleep
from day_to_day import views
from day_to_day import forms


class EmployeeView_test(TestCase):
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

    def test_get_permission(self):
        class Instance:
            def __init__(self, extra_context):
                self.extra_context = extra_context

        class Request:
            def __init__(self, user):
                self.user = user

        instance = Instance({"employe": ...})
        request = Request(self.user)
        views.get_permission(instance, request)
        self.assertEqual(instance.extra_context["employee"], self.user)
        instance = Instance({"employe": ...})
        request = Request(self.employee)
        views.get_permission(instance, request)
        self.assertEqual(
            str(instance.extra_context["employee"].pk), self.employee.pk
        )
        with self.assertRaises(PermissionDenied):
            instance = Instance({"employe": ...})
            request = Request(self.family_member)
            views.get_permission(instance, request)
        with self.assertRaises(Exception):
            views.get_permission(None, None)

    def test_employeepage_exists_access_employee_allowed(self):
        request = RequestFactory().get("/day-to-day/employe/")
        request.user = self.employee
        view = views.EmployeeView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_employeepage_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("d_to_d:employee"))
        request.user = self.employee
        view = views.EmployeeView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_employeepage_uses_correct_template(self):
        request = RequestFactory().get(reverse("d_to_d:employee"))
        request.user = self.employee
        view = views.EmployeeView()
        view.setup(request)
        self.assertEqual(view.template_name, "day_to_day/_employee_index.html")

    def test_permission_denied(self):
        with self.assertRaises(PermissionDenied):
            request = RequestFactory().get(reverse("d_to_d:employee"))
            request.user = self.family_member
            view = views.EmployeeView()
            view.setup(request)
            view.get(request)

    def test_employeepage_exists_access_superuser_allowed(self):
        request = RequestFactory().get("/day-to-day/employe/")
        request.user = self.user
        view = views.EmployeeView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get("/day-to-day/employe/")
        request.user = self.user
        view = views.EmployeeView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(
            list(view.extra_context.get("messages"))[0], self.message
        )
        self.assertEqual(view.extra_context.get("employee"), self.user)


class ChildListView_test(TestCase):
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

    def test_childlistpage_exists_access_employee_allowed(self):
        request = RequestFactory().get("/employe/enfants/")
        request.user = self.employee
        view = views.ChildListView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_childlistpage_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("d_to_d:child_list"))
        request.user = self.employee
        view = views.ChildListView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_childlistpage_uses_correct_template(self):
        request = RequestFactory().get(reverse("d_to_d:child_list"))
        request.user = self.employee
        view = views.ChildListView()
        view.setup(request)
        self.assertEqual(view.template_name, "day_to_day/_child_list.html")

    def test_permission_denied(self):
        with self.assertRaises(PermissionDenied):
            request = RequestFactory().get(reverse("d_to_d:child_list"))
            request.user = self.family_member
            view = views.ChildListView()
            view.setup(request)
            view.get(request)

    def test_childlistpage_exists_access_superuser_allowed(self):
        request = RequestFactory().get(reverse("d_to_d:child_list"))
        request.user = self.user
        view = views.ChildListView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(reverse("d_to_d:child_list"))
        request.user = self.user
        view = views.ChildListView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(view.extra_context.get("employee"), self.user)


class ChildTransmissionsView_test(TestCase):
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
        cls.child = Child.objects.create(
            first_name="prénom",
            last_name="Nom",
            birth_date="2020-12-20",
            vaccine_next_due_date="2020-12-20",
            cc_facility=cls.cc_facility,
        )

    def test_ChildTransmissionspage_exists_access_employee_allowed(self):
        pk = self.child.pk
        request = RequestFactory().get(
            "employe/enfants/" + str(pk) + "/transmissions/ajouter/False"
        )
        request.user = self.employee
        view = views.ChildTransmissionsView()
        view.setup(request)
        self.assertEqual(
            view.get(request, pk=pk, success=False).status_code, 200
        )

    def test_ChildTransmissionspage_url_accessible_by_name(self):
        response = self.client.get(
            reverse(
                "d_to_d:Child_transmissions",
                args=[self.child.pk, False],
                current_app="d_to_d",
            )
        )
        self.assertTrue(response.status_code, 200)

    def test_ChildTransmissions_page_uses_correct_template(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:Child_transmissions",
                args=[self.child.pk, False],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.ChildTransmissionsView()
        view.setup(request)
        self.assertEqual(view.template_name, "day_to_day/_trans_list.html")

    def test_permission_denied(self):
        with self.assertRaises(PermissionDenied):
            request = RequestFactory().get(
                reverse(
                    "d_to_d:Child_transmissions",
                    args=[self.child.pk, False],
                    current_app="d_to_d",
                )
            )
            request.user = self.family_member
            view = views.ChildTransmissionsView()
            view.setup(request)
            view.get(request, pk=self.child.pk, success=False)

    def test_ChildTransmissions_page_exists_access_superuser_allowed(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:Child_transmissions",
                args=[self.child.pk, False],
                current_app="d_to_d",
            )
        )
        request.user = self.user
        view = views.ChildTransmissionsView()
        view.setup(request)
        self.assertEqual(
            view.get(request, pk=self.child.pk, success=False).status_code, 200
        )

    def test_context_exists(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:Child_transmissions",
                args=[self.child.pk, False],
                current_app="d_to_d",
            )
        )
        request.user = self.user
        view = views.ChildTransmissionsView()
        view.setup(request)
        self.assertEqual(
            view.get(request, pk=self.child.pk, success=False).status_code, 200
        )
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(view.extra_context.get("employee"), self.user)
        self.assertEqual(view.extra_context.get("child"), self.child)
        self.assertEqual(
            view.extra_context.get("transmission_recorded", None), None
        )


class ChildView_test(TestCase):
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
        cls.child = Child.objects.create(
            first_name="prénom",
            last_name="Nom",
            birth_date="2020-12-20",
            vaccine_next_due_date="2020-12-20",
            cc_facility=cls.cc_facility,
        )
        cls.child.relative.add(
            cls.family_member,
            through_defaults={
                "link_type": "mère",
                "retrieval_auth": True,
                "emergency_contact_person": True,
            },
        )

    def test_ChildViewpage_exists_access_employee_allowed(self):
        pk = self.child.pk
        request = RequestFactory().get("employe/enfants/" + str(pk) + "/")
        request.user = self.employee
        view = views.ChildView()
        view.setup(request, pk=pk)
        self.assertEqual(view.get(request).status_code, 200)

    def test_ChildViewpage_url_accessible_by_name(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:Child_facts",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)

    def test_ChildViewpage_uses_correct_template(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:Child_facts",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.template_name, "day_to_day/_child_detail.html")

    def test_permission_denied(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:Child_facts",
                args=[str(self.child.pk)],
                current_app="d_to_d",
            )
        )
        request.user = self.family_member
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        try:
            view.get(request)
        except PermissionDenied:
            pass

    def test_ChildViewpage_exists_access_superuser_allowed(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:Child_facts",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.user
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:Child_facts",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.user
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(view.extra_context.get("employee"), self.user)
        self.assertEqual(
            list(view.extra_context.get("emergency_contacts"))[0],
            self.family_member,
        )
        self.assertEqual(
            list(view.extra_context.get("authorized_familly"))[0],
            self.family_member,
        )


class EmployeeTransmissionsListView_test(TestCase):
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
        cls.child = Child.objects.create(
            first_name="prénom",
            last_name="Nom",
            birth_date="2020-12-20",
            vaccine_next_due_date="2020-12-20",
            cc_facility=cls.cc_facility,
        )
        cls.child.relative.add(
            cls.family_member,
            through_defaults={
                "link_type": "mère",
                "retrieval_auth": True,
                "emergency_contact_person": True,
            },
        )

    def test_child_transmissions_add_page_exists_access_employee_allowed(self):
        request = RequestFactory().get("/employe/transmissions/")
        request.user = self.employee
        view = views.EmployeeTransmissionsListView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_child_transmissions_add_page_url_accessible_by_name(self):
        request = RequestFactory().get(
            reverse("d_to_d:tr_list", current_app="d_to_d")
        )
        request.user = self.employee
        view = views.EmployeeTransmissionsListView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_child_transmissions_add_page_uses_correct_template(self):
        request = RequestFactory().get(
            reverse("d_to_d:tr_list", current_app="d_to_d")
        )
        request.user = self.employee
        view = views.EmployeeTransmissionsListView()
        view.setup(request)
        self.assertEqual(
            view.template_name, "day_to_day/_employee_trans_list.html"
        )

    def test_permission_denied(self):
        request = RequestFactory().get(
            reverse("d_to_d:tr_list", current_app="d_to_d")
        )
        request.user = self.family_member
        view = views.EmployeeTransmissionsListView()
        view.setup(request)
        try:
            view.get(request)
        except PermissionDenied:
            pass

    def test_child_transmissions_add_page_exists_access_superuser_allowed(
        self,
    ):
        request = RequestFactory().get(
            reverse("d_to_d:tr_list", current_app="d_to_d")
        )
        request.user = self.user
        view = views.EmployeeTransmissionsListView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(
            reverse("d_to_d:tr_list", current_app="d_to_d")
        )
        request.user = self.user
        view = views.EmployeeTransmissionsListView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(view.extra_context.get("employee"), self.user)


class ChildTransmissionsAddView_test(TestCase):
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
        cls.child = Child.objects.create(
            first_name="prénom",
            last_name="Nom",
            birth_date="2020-12-20",
            vaccine_next_due_date="2020-12-20",
            cc_facility=cls.cc_facility,
        )
        cls.child.relative.add(
            cls.family_member,
            through_defaults={
                "link_type": "mère",
                "retrieval_auth": True,
                "emergency_contact_person": True,
            },
        )

    def test_child_transmissions_add_page_exists_access_employee_allowed(self):
        request = RequestFactory().get(
            "employe/enfants/" + str(self.child.pk) + "/transmissions/ajouter/"
        )
        request.user = self.employee
        view = views.ChildTransmissionsAddView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.child.pk).status_code, 200)

    def test_child_transmissions_add_page_url_accessible_by_name(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmission_add",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.ChildTransmissionsAddView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.child.pk).status_code, 200)

    def test_child_transmissions_add_page_uses_correct_template(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmission_add",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.ChildTransmissionsAddView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.template_name, "day_to_day/_trans_add.html")

    def test_permission_denied(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmission_add",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.family_member
        view = views.ChildTransmissionsAddView()
        view.setup(request)
        try:
            view.get(request, pk=self.child.pk)
        except PermissionDenied:
            pass

    def test_child_transmissions_add_page_exists_access_superuser_allowed(
        self,
    ):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmission_add",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.user
        view = views.ChildTransmissionsAddView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.child.pk).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmission_add",
                args=[self.child.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.user
        view = views.ChildTransmissionsAddView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.child.pk).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(view.extra_context.get("employee"), self.user)
        self.assertEqual(view.extra_context.get("message"), None)
        self.assertEqual(view.extra_context.get("child"), self.child)
        self.assertIsInstance(
            view.extra_context.get("sleep_form"), type(forms.SleepFormSet())
        )
        self.assertIsInstance(
            view.extra_context.get("meal_form"), type(forms.MealFormSet())
        )
        self.assertIsInstance(
            view.extra_context.get("activity_form"),
            type(forms.ActivityFormSet()),
        )
        self.assertIsInstance(
            view.extra_context.get("feeding_bttle_form"),
            type(forms.FeedingBottleFormSet()),
        )
        self.assertIsInstance(
            view.extra_context.get("medical_form"),
            type(forms.MedicalEventFormSet()),
        )

    def test_post_request(self):
        request = RequestFactory().post(
            reverse(
                "d_to_d:transmission_add",
                args=[self.child.pk],
                current_app="d_to_d",
            ),
            data={
                "comment": "abc",
            },
        )
        request.user = self.employee
        view = views.ChildTransmissionsAddView()
        view.setup(request)

        class DailyFactForm_mock:
            @classmethod
            def form_is_valid_mock(*args, **kwargs):
                return True

            @classmethod
            def form_is_not_valid_mock(*args, **kwargs):
                return False

            def form_save_mock(self, *args, **kwargs):
                return DailyFact.objects.create(
                    employee=self.data["employee"],
                    child=self.data["child"],
                    comment=self.data["comment"],
                )

            def form_delete_mock(self, *args, **kwargs):
                DailyFact.objects.all().delete()

        class Formset_mock:
            @classmethod
            def is_valid(*args, **kwargs):
                return True

            @classmethod
            def is_not_valid(*args, **kwargs):
                return False

            @classmethod
            def save(*args, **kwargs):
                return True

        with mock.patch(
            "day_to_day.forms.DailyFactForm.is_valid",
            new=DailyFactForm_mock.form_is_valid_mock,
        ), mock.patch(
            "day_to_day.forms.DailyFactForm.save",
            new=DailyFactForm_mock.form_save_mock,
        ), mock.patch(
            "day_to_day.forms.SleepFormSet.is_valid", new=Formset_mock.is_valid
        ), mock.patch(
            "day_to_day.forms.MealFormSet.is_valid", new=Formset_mock.is_valid
        ), mock.patch(
            "day_to_day.forms.ActivityFormSet.is_valid",
            new=Formset_mock.is_valid,
        ), mock.patch(
            "day_to_day.forms.FeedingBottleFormSet.is_valid",
            new=Formset_mock.is_valid,
        ), mock.patch(
            "day_to_day.forms.MedicalEventFormSet.is_valid",
            new=Formset_mock.is_valid,
        ), mock.patch(
            "day_to_day.forms.SleepFormSet.save", new=Formset_mock.save
        ), mock.patch(
            "day_to_day.forms.MealFormSet.save", new=Formset_mock.save
        ), mock.patch(
            "day_to_day.forms.ActivityFormSet.save", new=Formset_mock.save
        ), mock.patch(
            "day_to_day.forms.FeedingBottleFormSet.save", new=Formset_mock.save
        ), mock.patch(
            "day_to_day.forms.MedicalEventFormSet.save", new=Formset_mock.save
        ):

            self.assertEqual(
                view.post(request, pk=self.child.pk).status_code, 302
            )
            self.assertEqual(
                DailyFact.objects.get(child=self.child).comment, "abc"
            )

        with mock.patch(
            "day_to_day.forms.DailyFactForm.is_valid",
            new=DailyFactForm_mock.form_is_not_valid_mock,
        ):

            self.assertEqual(
                view.post(request, pk=self.child.pk).status_code, 200
            )
            self.assertEqual(
                view.extra_context.get("message"),
                "Veuillez corriger les erreurs dans le commentaire",
            )

        with mock.patch(
            "day_to_day.forms.DailyFactForm.is_valid",
            new=DailyFactForm_mock.form_is_valid_mock,
        ), mock.patch(
            "day_to_day.models.DailyFact.delete",
            new=DailyFactForm_mock.form_delete_mock,
        ), mock.patch(
            "day_to_day.forms.DailyFactForm.save",
            new=DailyFactForm_mock.form_save_mock,
        ), mock.patch(
            "day_to_day.forms.SleepFormSet.is_valid",
            new=Formset_mock.is_not_valid,
        ), mock.patch(
            "day_to_day.forms.MealFormSet.is_valid",
            new=Formset_mock.is_not_valid,
        ), mock.patch(
            "day_to_day.forms.ActivityFormSet.is_valid",
            new=Formset_mock.is_not_valid,
        ), mock.patch(
            "day_to_day.forms.FeedingBottleFormSet.is_valid",
            new=Formset_mock.is_not_valid,
        ), mock.patch(
            "day_to_day.forms.MedicalEventFormSet.is_valid",
            new=Formset_mock.is_not_valid,
        ):

            self.assertEqual(
                view.post(request, pk=self.child.pk).status_code, 200
            )
            self.assertIsInstance(
                view.extra_context.get("sleep_form"),
                type(forms.SleepFormSet()),
            )
            self.assertIsInstance(
                view.extra_context.get("meal_form"), type(forms.MealFormSet())
            )
            self.assertIsInstance(
                view.extra_context.get("activity_form"),
                type(forms.ActivityFormSet()),
            )
            self.assertIsInstance(
                view.extra_context.get("feeding_bttle_form"),
                type(forms.FeedingBottleFormSet()),
            )
            self.assertIsInstance(
                view.extra_context.get("medical_form"),
                type(forms.MedicalEventFormSet()),
            )
            self.assertEqual(
                view.extra_context.get("message"),
                "Veuillez corriger les erreurs dans les champs suivants : "
                + "Sieste, Repas, Activités, Biberons, Médical",
            )
            self.assertEqual(view.extra_context.get("post"), True)
            self.assertEqual(DailyFact.objects.all().count(), 0)


class TransmissionsChangeView(TestCase):
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
        cls.child = Child.objects.create(
            first_name="prénom",
            last_name="Nom",
            birth_date="2020-12-20",
            vaccine_next_due_date="2020-12-20",
            cc_facility=cls.cc_facility,
        )
        cls.child.relative.add(
            cls.family_member,
            through_defaults={
                "link_type": "mère",
                "retrieval_auth": True,
                "emergency_contact_person": True,
            },
        )
        cls.trans = DailyFact.objects.create(
            employee=cls.employee, child=cls.child, comment="abc"
        )

    def test_transmissions_change_page_exists_access_employee_allowed(self):
        request = RequestFactory().get(
            "employe/transmission/modifier/" + str(self.trans.pk)
        )
        request.user = self.employee
        view = views.TransmissionsChangeView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.trans.pk).status_code, 200)

    def test_transmissions_change_page_url_accessible_by_name(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.TransmissionsChangeView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.trans.pk).status_code, 200)

    def test_transmissions_change_page_uses_correct_template(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.TransmissionsChangeView()
        view.setup(request, pk=self.trans.pk)
        self.assertEqual(view.template_name, "day_to_day/_trans_detail.html")

    def test_permission_denied(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.family_member
        view = views.TransmissionsChangeView()
        view.setup(request)
        try:
            view.get(request, pk=self.trans.pk)
        except PermissionDenied:
            pass

    def test_transmissions_change_page_exists_access_superuser_allowed(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.user
        view = views.TransmissionsChangeView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.trans.pk).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.user
        view = views.TransmissionsChangeView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.trans.pk).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(view.extra_context.get("employee"), self.user)
        self.assertEqual(view.extra_context.get("success"), False)
        self.assertEqual(view.extra_context.get("transmission_recorded"), None)
        self.assertEqual(view.extra_context.get("trans"), self.trans)
        self.assertEqual(
            view.extra_context.get("sleep_form").instance, self.trans
        )
        self.assertEqual(
            view.extra_context.get("meal_form").instance, self.trans
        )
        self.assertEqual(
            view.extra_context.get("activity_form").instance, self.trans
        )
        self.assertEqual(
            view.extra_context.get("feeding_bttle_form").instance, self.trans
        )
        self.assertEqual(
            view.extra_context.get("medical_form").instance, self.trans
        )

    @mock.patch("day_to_day.views.TransmissionsChangeView.get_formset")
    @mock.patch("day_to_day.views.SleepFormSet")
    def test_post_request_is_valid_formset(
        self, mock_get_formset, mock_SleepFormSet
    ):
        request = RequestFactory().post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        formset = [
            ["sleep_form", "Sieste"],
            forms.SleepFormSet(request.POST, instance=self.trans),
        ]
        mock_get_formset.side_effect = [formset, True]
        mock_SleepFormSet.save = DailyFact.objects.create(
            employee=self.employee,
            child=self.child,
            comment="new_trans",
        )
        request.user = self.employee
        view = views.TransmissionsChangeView()
        view.setup(request)
        self.assertEqual(view.post(request, pk=self.trans.pk).status_code, 302)
        self.assertEqual(view.extra_context.get("success"), True)
        self.assertIsInstance(
            DailyFact.objects.get(comment="new_trans"), DailyFact
        )

    @mock.patch("day_to_day.views.TransmissionsChangeView.get_formset")
    def test_post_request_is_valid_form(self, mock_get_formset):
        request = RequestFactory().post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        formset = [
            ["form", "Commentaire"],
            forms.DailyFactForm(
                data={
                    "child": self.trans.child,
                    "employee": self.employee,
                    "comment": "new_trans",
                }
            ),
        ]
        mock_get_formset.side_effect = [formset, True, "form"]
        request.user = self.employee
        view = views.TransmissionsChangeView()
        view.setup(request)
        self.assertEqual(view.post(request, pk=self.trans.pk).status_code, 302)
        self.assertEqual(view.extra_context.get("success"), True)
        self.assertEqual(DailyFact.objects.get(pk=self.trans.pk), self.trans)
        self.assertIsInstance(
            DailyFact.objects.get(comment="new_trans"), DailyFact
        )

    @mock.patch("day_to_day.views.TransmissionsChangeView.form_invalid")
    def test_post_request_is_not_valid(self, mock_form_invalid):
        request = RequestFactory().post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.TransmissionsChangeView()
        view.setup(request)
        mock_form_invalid.side_effect = Exception
        with self.assertRaises(Exception):
            self.assertEqual(
                view.post(request, pk=self.trans.pk).status_code, 200
            )
            self.assertEqual(view.extra_context.get("success"), False)
            mock_form_invalid.assert_called_once()

        with self.assertRaises(ObjectDoesNotExist):
            daily_fact = DailyFact.objects.get(pk=self.trans.pk)
            Sleep.objects.get(daily_fact=daily_fact)

    def test_form_invalid(self):
        request = RequestFactory().post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.TransmissionsChangeView()
        view.setup(request)
        self.assertEqual(view.post(request, pk=self.trans.pk).status_code, 200)
        self.assertIsInstance(
            view.form_invalid([["formset", "Commentaire"], "dummy_formset"]),
            HttpResponse,
        )
        result = (
            view.form_invalid([["form", "Commentaire"], "dummy_formset"]),
        )
        self.assertEqual(
            result[0].context_data.get("message"),
            "La modification de la donnée Commentaire n'a pas été effectuée "
            + "merci de vérifier les erreurs",
        )
        self.assertEqual(
            result[0].context_data.get("formset"),
            "dummy_formset",
        )

    def test_get_formset(self):
        request = RequestFactory().post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            )
        )
        request.user = self.employee
        view = views.TransmissionsChangeView()
        view.setup(request)
        self.assertEqual(view.post(request, pk=self.trans.pk).status_code, 200)
        formdict = {
            "sleep_set-TOTAL_FORMS": [
                ["sleep_form", "Sieste"],
                forms.SleepFormSet(),
            ],
            "meal_set-TOTAL_FORMS": [
                ["meal_form", "Repas"],
                forms.MealFormSet(),
            ],
            "activity_set-TOTAL_FORMS": [
                ["activity_form", "Activités"],
                forms.ActivityFormSet(),
            ],
            "feedingbottle_set-TOTAL_FORMS": [
                ["feeding_bttle_form", "Biberons"],
                forms.FeedingBottleFormSet(),
            ],
            "medicalevent_set-TOTAL_FORMS": [
                ["medical_form", "Médical"],
                forms.MedicalEventFormSet(),
            ],
        }
        for key, data in formdict.items():
            result = (
                view.get_formset(
                    {key: "xxx", "comment": "comment"}, self.user
                ),
            )
            self.assertEqual(result[0][0], data[0])
            self.assertIsInstance(result[0][1], type(data[1]))


class ParentView(TestCase):
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
        cls.child = Child.objects.create(
            first_name="prénom",
            last_name="Nom",
            birth_date="2020-12-20",
            vaccine_next_due_date="2020-12-20",
            cc_facility=cls.cc_facility,
        )
        cls.child.relative.add(
            cls.family_member,
            through_defaults={
                "link_type": "mère",
                "retrieval_auth": True,
                "emergency_contact_person": True,
            },
        )
        cls.trans = DailyFact.objects.create(
            employee=cls.employee, child=cls.child, comment="abc"
        )

    def test_ParentView_page_exists_access_parent_allowed(self):
        request = RequestFactory().get("parent/")
        request.user = self.family_member
        view = views.ParentView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_ParentView_page_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("d_to_d:parent"))
        request.user = self.family_member
        view = views.ParentView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_ParentView_page_uses_correct_template(self):
        request = RequestFactory().get(reverse("d_to_d:parent"))
        request.user = self.family_member
        view = views.ParentView()
        view.setup(request)
        self.assertEqual(
            view.template_name, "day_to_day/_parent_trans_list.html"
        )

    def test_permission_denied(self):
        request = RequestFactory().get(reverse("d_to_d:parent"))
        request.user = self.employee
        view = views.ParentView()
        view.setup(request)
        try:
            view.get(request)
        except PermissionDenied:
            pass

    def test_ParentView_page_exists_access_superuser_allowed(self):
        request = RequestFactory().get(reverse("d_to_d:parent"))
        request.user = self.user
        view = views.ParentView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(reverse("d_to_d:parent"))
        request.user = self.family_member
        view = views.ParentView()
        view.setup(request)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(view.extra_context.get("parent"), self.family_member)
        self.assertEqual(view.extra_context.get("childs")[0], self.child)


class Child_transmissions_report(TestCase):
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
        cls.child = Child.objects.create(
            first_name="prénom",
            last_name="Nom",
            birth_date="2020-12-20",
            vaccine_next_due_date="2020-12-20",
            cc_facility=cls.cc_facility,
        )
        cls.child.relative.add(
            cls.family_member,
            through_defaults={
                "link_type": "mère",
                "retrieval_auth": True,
                "emergency_contact_person": True,
            },
        )
        cls.trans = DailyFact.objects.create(
            employee=cls.employee, child=cls.child, comment="abc"
        )

    def test_Child_transmissions_report_page_exists_access_parent_allowed(
        self,
    ):
        request = RequestFactory().get("child/" + str(self.child.pk) + "/")
        request.user = self.family_member
        view = views.Child_transmissions_report()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)

    def Child_transmissions_report_page_url_accessible_by_name(self):
        request = RequestFactory().get(
            reverse("d_to_d:child", args=[self.child.pk])
        )
        request.user = self.family_member
        view = views.Child_transmissions_report()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)

    def Child_transmissions_report_page_uses_correct_template(self):
        request = RequestFactory().get(
            reverse("d_to_d:child", args=[self.child.pk])
        )
        request.user = self.family_member
        view = views.Child_transmissions_report()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(
            view.template_name, "day_to_day/_parent_trans_list.html"
        )

    def test_permission_denied(self):
        request = RequestFactory().get(
            reverse("d_to_d:child", args=[self.child.pk])
        )
        request.user = self.employee
        view = views.Child_transmissions_report()
        view.setup(request, pk=self.child.pk)
        try:
            view.get(request)
        except PermissionDenied:
            pass

    def Child_transmissions_report_page_exists_access_superuser_allowed(self):
        request = RequestFactory().get(
            reverse("d_to_d:child", args=[self.child.pk])
        )
        request.user = self.user
        view = views.Child_transmissions_report()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(
            reverse("d_to_d:child", args=[self.child.pk])
        )
        request.user = self.family_member
        view = views.Child_transmissions_report()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertEqual(
            view.extra_context.get("child_care_facility"), self.cc_facility
        )
        self.assertEqual(view.object_list[0], self.trans)
        self.assertEqual(view.extra_context.get("child"), self.child)
