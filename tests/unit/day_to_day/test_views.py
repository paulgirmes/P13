"""
unit tests for day_to_day views
"""

from unittest import mock

from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.test import TestCase, override_settings, RequestFactory
from frontpage.models import New, Child_care_facility, User
from auth_access_admin.models import Address, Employee, FamilyMember
from day_to_day.models import Message, Child
from day_to_day import views


class EmployeeView_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "superuser@hotmail.com",
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789879/",
            email = "nomprenom@hotmail.com",
            is_superuser = True,
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
        cls.message = Message.objects.create(
            cc_facility = cls.cc_facility,
            title = "title",
            content = "content"
        )
        cls.employee = Employee.objects.create_user(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "employe@hotmail.com",
            phone = 13510006788,
            IdScan = "/fakepath/jfoijhzefe.jpg",
            occupation = "healthcare",
            employee_nr = "12313",
            diploma = "CPA",
            Is_manager = True,
            employee_contract = "/fakepath/jfoijhzefe.jpg",
            address = cls.address
        )
        cls.family_member = FamilyMember.objects.create(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "nomprenom@hotmail.com",
            phone = 13510006788,
            IdScan = "/fakepath/jfoijhzefe.jpg",
            has_daylyfact_access = True,
            address = cls.address,
        )

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
        self.assertEqual(view.template_name , "day_to_day/_employee_index.html")

    def test_permission_denied(self):
        try:
            request = RequestFactory().get(reverse("d_to_d:employee"))
            request.user = self.family_member
            view = views.EmployeeView()
        except:
            self.assertRaises(PermissionDenied, view.get(request))

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
        self.assertTrue(view.extra_context.get("child_care_facility"), self.cc_facility)
        self.assertTrue(view.extra_context.get("messages"), self.message)
        self.assertTrue(view.extra_context.get("employee"), self.user)


class ChildListView_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "superuser@hotmail.com",
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789879/",
            email = "nomprenom@hotmail.com",
            is_superuser = True,
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
        cls.message = Message.objects.create(
            cc_facility = cls.cc_facility,
            title = "title",
            content = "content"
        )
        cls.employee = Employee.objects.create_user(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "employe@hotmail.com",
            phone = 13510006788,
            IdScan = "/fakepath/jfoijhzefe.jpg",
            occupation = "healthcare",
            employee_nr = "12313",
            diploma = "CPA",
            Is_manager = True,
            employee_contract = "/fakepath/jfoijhzefe.jpg",
            address = cls.address
        )
        cls.family_member = FamilyMember.objects.create(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "nomprenom@hotmail.com",
            phone = 13510006788,
            IdScan = "/fakepath/jfoijhzefe.jpg",
            has_daylyfact_access = True,
            address = cls.address,
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
        self.assertEqual(view.template_name , "day_to_day/_child_list.html")

    def test_permission_denied(self):
        try:
            request = RequestFactory().get(reverse("d_to_d:child_list"))
            request.user = self.family_member
            view = views.ChildListView()
        except:
            self.assertRaises(PermissionDenied, view.get(request))

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
        self.assertTrue(view.extra_context.get("child_care_facility"), self.cc_facility)
        self.assertTrue(view.extra_context.get("employee"), self.user)


class ChildTransmissionsView_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "superuser@hotmail.com",
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789879/",
            email = "nomprenom@hotmail.com",
            is_superuser = True,
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
        cls.message = Message.objects.create(
            cc_facility = cls.cc_facility,
            title = "title",
            content = "content"
        )
        cls.employee = Employee.objects.create_user(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "employe@hotmail.com",
            phone = 13510006788,
            IdScan = "/fakepath/jfoijhzefe.jpg",
            occupation = "healthcare",
            employee_nr = "12313",
            diploma = "CPA",
            Is_manager = True,
            employee_contract = "/fakepath/jfoijhzefe.jpg",
            address = cls.address
        )
        cls.family_member = FamilyMember.objects.create(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "nomprenom@hotmail.com",
            phone = 13510006788,
            IdScan = "/fakepath/jfoijhzefe.jpg",
            has_daylyfact_access = True,
            address = cls.address,
        )
        cls.child = Child.objects.create(
            first_name = "prénom",
            last_name = "Nom",
            birth_date = "2020-12-20",
            vaccine_next_due_date = "2020-12-20",
            cc_facility = cls.cc_facility,
        )

    def test_ChildTransmissionspage_exists_access_employee_allowed(self):
        pk = self.child.pk
        request = RequestFactory().get("employe/enfants/"+str(pk)+"/transmissions/ajouter/False")
        request.user = self.employee
        view = views.ChildTransmissionsView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=pk, success=False).status_code, 200)

    def test_ChildTransmissionspage_url_accessible_by_name(self):
        response = self.client.get(reverse("d_to_d:Child_transmissions", args=[self.child.pk, False], current_app="d_to_d"))
        self.assertTrue(response.status_code , 200)

    def test_ChildTransmissionspage_uses_correct_template(self):
        request = RequestFactory().get(reverse("d_to_d:Child_transmissions", args=[self.child.pk, False], current_app="d_to_d"))
        request.user = self.employee
        view = views.ChildTransmissionsView()
        view.setup(request)
        self.assertEqual(view.template_name , "day_to_day/_trans_list.html")

    def test_permission_denied(self):
        try:
            request = RequestFactory().get(reverse("d_to_d:Child_transmissions", args=[self.child.pk, False], current_app="d_to_d"))
            request.user = self.family_member
            view = views.ChildTransmissionsView()
        except:
            self.assertRaises(PermissionDenied, view.get(request, pk=self.child.pk, success=False))

    def test_ChildTransmissionspage_exists_access_superuser_allowed(self):
        request = RequestFactory().get(reverse("d_to_d:Child_transmissions", args=[self.child.pk, False], current_app="d_to_d"))
        request.user = self.user
        view = views.ChildTransmissionsView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.child.pk, success=False).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(reverse("d_to_d:Child_transmissions", args=[self.child.pk, False], current_app="d_to_d"))
        request.user = self.user
        view = views.ChildTransmissionsView()
        view.setup(request)
        self.assertEqual(view.get(request, pk=self.child.pk, success=False).status_code, 200)
        self.assertTrue(view.extra_context.get("child_care_facility"), self.cc_facility)
        self.assertTrue(view.extra_context.get("employee"), self.user)
        self.assertTrue(view.extra_context.get("child"), self.child)
        self.assertEqual(view.extra_context.get("transmission_recorded", None), None)


class ChildView_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "superuser@hotmail.com",
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789879/",
            email = "nomprenom@hotmail.com",
            is_superuser = True,
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
        cls.message = Message.objects.create(
            cc_facility = cls.cc_facility,
            title = "title",
            content = "content"
        )
        cls.employee = Employee.objects.create_user(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "employe@hotmail.com",
            phone = 13510006788,
            IdScan = "/fakepath/jfoijhzefe.jpg",
            occupation = "healthcare",
            employee_nr = "12313",
            diploma = "CPA",
            Is_manager = True,
            employee_contract = "/fakepath/jfoijhzefe.jpg",
            address = cls.address
        )
        cls.family_member = FamilyMember.objects.create(
            first_name = "prénom",
            last_name = "Nom",
            password = "123456789",
            username = "nomprenom@hotmail.com",
            phone = 13510006788,
            IdScan = "/fakepath/jfoijhzefe.jpg",
            has_daylyfact_access = True,
            address = cls.address,
        )
        cls.child = Child.objects.create(
            first_name = "prénom",
            last_name = "Nom",
            birth_date = "2020-12-20",
            vaccine_next_due_date = "2020-12-20",
            cc_facility = cls.cc_facility,
        )
        cls.child.relative.add(cls.family_member, through_defaults={
            "link_type":"mère",
            "retrieval_auth":True,
            "emergency_contact_person":True,
            }
        )

    def test_ChildViewpage_exists_access_employee_allowed(self):
        pk = self.child.pk
        request = RequestFactory().get("employe/enfants/"+str(pk)+"/")
        request.user = self.employee
        view = views.ChildView()
        view.setup(request, pk=pk)
        self.assertEqual(view.get(request).status_code, 200)

    def test_ChildViewpage_url_accessible_by_name(self):
        request = RequestFactory().get(reverse("d_to_d:Child_facts", args=[self.child.pk], current_app="d_to_d"))
        request.user = self.employee
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)

    def test_ChildViewpage_uses_correct_template(self):
        request = RequestFactory().get(reverse("d_to_d:Child_facts", args=[self.child.pk], current_app="d_to_d"))
        request.user = self.employee
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.template_name , "day_to_day/_child_detail.html")

    def test_permission_denied(self):
        request = RequestFactory().get(reverse("d_to_d:Child_facts", args=[str(self.child.pk)], current_app="d_to_d"))
        request.user = self.family_member
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        try:
            view.get(request)
        except PermissionDenied as e:
            pass


    def test_ChildViewpage_exists_access_superuser_allowed(self):
        request = RequestFactory().get(reverse("d_to_d:Child_facts", args=[self.child.pk], current_app="d_to_d"))
        request.user = self.user
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)

    def test_context_exists(self):
        request = RequestFactory().get(reverse("d_to_d:Child_facts", args=[self.child.pk], current_app="d_to_d"))
        request.user = self.user
        view = views.ChildView()
        view.setup(request, pk=self.child.pk)
        self.assertEqual(view.get(request).status_code, 200)
        self.assertTrue(view.extra_context.get("child_care_facility"), self.cc_facility)
        self.assertTrue(view.extra_context.get("employee"), self.user)
        self.assertTrue(view.extra_context.get("emergency_contacts"), self.family_member)
        self.assertTrue(view.extra_context.get("authorized_familly", None), None)