"""
unit tests for auth_access_admin forms
"""

from unittest import mock
from django.test import SimpleTestCase, TestCase
from auth_access_admin.forms import (Login, Password_reset_form,
                                     EmployeeCreationForm, FamilyCreationForm,
                                     NewForm, DailyFactForm)
from auth_access_admin.models import Address, Employee
from frontpage.models import User, Child_care_facility


class LoginTest(SimpleTestCase):
    def test_username_widget(self):
        form = Login()
        self.assertEqual(
            form.fields["username"].widget.template_name,
            "django/forms/widgets/text.html",
        )
        self.assertEqual(
            form.fields["username"].widget.attrs, {
                'autofocus': True,
                'class': "form-control form-control-user",
                'autocapitalize': 'none',
                "autocomplete": 'username',
                'placeholder': "Entrez Votre Adresse Email",
                'maxlength': 254,
            })

    def test_password_widget(self):
        form = Login()
        self.assertEqual(
            form.fields["password"].widget.template_name,
            "django/forms/widgets/password.html",
        )
        self.assertEqual(
            form.fields["password"].widget.attrs, {
                'autocomplete': 'current-password',
                'class': "form-control form-control-user",
                'placeholder': "Entrez Votre Mot de Passe",
            })


class Password_reset_formTest(TestCase):
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

    def test_new_password1_widget(self):
        form = Password_reset_form(self.user)
        self.assertEqual(
            form.fields["new_password1"].widget.template_name,
            "django/forms/widgets/password.html",
        )
        self.assertEqual(
            form.fields["new_password1"].widget.attrs, {
                'autocomplete': 'new-password',
                'class': "form-control form-control-user",
            })

    def test_new_password2_widget(self):
        form = Password_reset_form(self.user)
        self.assertEqual(
            form.fields["new_password2"].widget.template_name,
            "django/forms/widgets/password.html",
        )
        self.assertEqual(
            form.fields["new_password2"].widget.attrs, {
                'autocomplete': 'new-password',
                'class': "form-control form-control-user",
            })


class EmployeeCreationFormTest(TestCase):
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
            postal_code="31300"
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

    def test_fields(self):
        form = EmployeeCreationForm()
        self.assertEqual(
            form.Meta.fields,
            (
                "username",
                "first_name",
                "last_name",
                "phone",
                "IdScan",
                "address",
                "occupation",
                "diploma",
                "employee_contract",
            ),
        )

    @mock.patch("auth_access_admin.forms.UserCreationForm.save")
    def test_save(self, mock_save):
        form = EmployeeCreationForm(data={
            "first_name": "prénom",
            "last_name": "Nom",
            "password1": "123456789//",
            "password2": "123456789//",
            "username": "employe15@hotmail.com",
            "email": "employe15@hotmail.com",
            "phone": 13510006788,
            "IdScan": self.employee.IdScan,
            "occupation": "healthcare",
            "employee_nr": "12313",
            "diploma": "CPA",
            "Is_manager": True,
            "employee_contract": self.employee.employee_contract,
            "address": self.address
        })

        class MockUser():
            saved = None
            employee_nr = None
            password = None

            def __init__(self, form):
                form.cleaned_data = {"password1": "password1"}

            def set_password(self, passwd):
                self.password = passwd

            def save(self):
                self.saved = True
        mock_save.side_effect = [MockUser(form), MockUser(form)]
        user = form.save()
        mock_save.assert_called_once()
        self.assertEqual(user.password, "password1")
        self.assertEqual(user.employee_nr, Employee.objects.order_by(
            "employee_nr").last().employee_nr+1)
        user = form.save(commit=False)
        self.assertEqual(user.saved, None)


class FamilyCreationFormTest(SimpleTestCase):

    def test_fields(self):
        form = FamilyCreationForm()
        self.assertEqual(
            form.Meta.fields,
            (
                "username",
                "first_name",
                "last_name",
                "phone",
                "IdScan",
                "address",
                "has_daylyfact_access",
            ),
        )


class NewFormTest(SimpleTestCase):

    def test_fields(self):
        form = NewForm()
        self.assertEqual(
            form.Meta.fields,
            "__all__",
        )


class DailyFactFormTest(SimpleTestCase):

    def test_comment_widget(self):
        form = DailyFactForm()
        self.assertEqual(
            form.fields["comment"].widget.template_name,
            "django/forms/widgets/textarea.html",
        )
        self.assertEqual(
            form.fields["comment"].widget.attrs, {
                'cols': 40, 'rows': 5,
                'maxlength': '200',
                'class': "form-control form-control-user",
                'placeholder': "Votre commentaire",
            })
