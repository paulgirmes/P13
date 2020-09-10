"""
Functionnal tests CC_ERP :
"""


import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from auth_access_admin.models import Address, Employee, FamilyMember
from day_to_day.models import Child, Message
from frontpage.models import Child_care_facility, User


class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_script_timeout(10)
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
            username="employenotmaanager@hotmail.com",
            phone=13510006788,
            IdScan="/fakepath/jfoijhzefe.jpg",
            occupation="healthcare",
            employee_nr="12",
            diploma="CPA",
            Is_manager=False,
            employee_contract="/fakepath/jfoijhzefe.jpg",
            address=cls.address,
            cc_facility=cls.cc_facility,
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

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_manager_employee(self):
        timeout = 5
        self.selenium.get("%s%s" % (self.live_server_url, "/"))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(
                By.CLASS_NAME, "sidebar-nav-item"
            )
        )
        toggle_btn = self.selenium.find_element(By.CLASS_NAME, "menu-toggle")
        toggle_btn.click()
        login = self.selenium.find_element(By.ID, "login")
        login.click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(By.ID, "id_username")
        )
        username_form = self.selenium.find_element(By.ID, "id_username")
        password_form = self.selenium.find_element(By.ID, "id_password")
        username_form.send_keys("employe@hotmail.com")
        password_form.send_keys("123456789" + Keys.ENTER)
        time.sleep(3)
        self.assertURLEqual(
            self.selenium.current_url,
            "%s%s" % (self.live_server_url, "/auth/index/"),
        )
        time.sleep(1)


class SeleniumTests2(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_script_timeout(10)
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
            username="employenotmanager@hotmail.com",
            phone=13510006788,
            IdScan="/fakepath/jfoijhzefe.jpg",
            occupation="healthcare",
            employee_nr="12",
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

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_not_manager_employee(self):
        timeout = 5
        self.selenium.get("%s%s" % (self.live_server_url, "/"))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(
                By.CLASS_NAME, "sidebar-nav-item"
            )
        )
        toggle_btn = self.selenium.find_element(By.CLASS_NAME, "menu-toggle")
        toggle_btn.click()
        login = self.selenium.find_element(By.ID, "login")
        login.click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(By.ID, "id_username")
        )
        username_form = self.selenium.find_element(By.ID, "id_username")
        password_form = self.selenium.find_element(By.ID, "id_password")
        username_form.send_keys("employenotmanager@hotmail.com")
        password_form.send_keys("123456789" + Keys.ENTER)
        time.sleep(3)
        self.assertURLEqual(
            self.selenium.current_url,
            "%s%s" % (self.live_server_url, "/day-to-day/employe/"),
        )
        time.sleep(1)


class SeleniumTests3(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_script_timeout(10)
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

        cls.family_member = FamilyMember.objects.create_user(
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

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_family_member_has_access(self):
        timeout = 5
        self.selenium.get("%s%s" % (self.live_server_url, "/"))

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(
                By.CLASS_NAME, "sidebar-nav-item"
            )
        )
        toggle_btn = self.selenium.find_element(By.CLASS_NAME, "menu-toggle")
        toggle_btn.click()
        login = self.selenium.find_element(By.ID, "login")
        login.click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element(By.ID, "id_username")
        )
        username_form = self.selenium.find_element(By.ID, "id_username")
        password_form = self.selenium.find_element(By.ID, "id_password")
        username_form.send_keys("nomprenom@hotmail.com")
        password_form.send_keys("123456789" + Keys.ENTER)
        time.sleep(3)
        self.assertURLEqual(
            self.selenium.current_url,
            "%s%s" % (self.live_server_url, "/day-to-day/parent/"),
        )
        time.sleep(1)
