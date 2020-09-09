"""
unit tests for day_to_day models
"""

from django.test import TestCase
from django.conf import settings
from day_to_day.models import (
    Child,
    Family_link,
    DailyFact,
    Sleep,
    Meal,
    FeedingBottle,
    Activity,
    MedicalEvent,
    Message,
)
from frontpage.models import Child_care_facility
from auth_access_admin.models import Address, FamilyMember, Employee


class Child_test(TestCase):
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
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
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

    def test_str(self):
        self.assertEqual(
            str(self.child), self.child.first_name + " " + self.child.last_name
        )

    def test_first_name_label(self):
        field_label = self.child._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "Prénom")

    def test_last_name_label(self):
        field_label = self.child._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "Nom")

    def test_birth_date_label(self):
        field_label = self.child._meta.get_field("birth_date").verbose_name
        self.assertEqual(field_label, "Date de Naissance")

    def test_vaccine_next_due_date_label(self):
        field_label = self.child._meta.get_field(
            "vaccine_next_due_date"
        ).verbose_name
        self.assertEqual(field_label, "Date de Prochaine Vaccination")

    def test_cc_facility_label(self):
        field_label = self.child._meta.get_field("cc_facility").verbose_name
        self.assertEqual(field_label, "Structure de Garde")

    def test_relative_label(self):
        field_label = self.child._meta.get_field("relative").verbose_name
        self.assertEqual(field_label, "Liens Familiaux")


class Family_link_test(TestCase):
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
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
            address=cls.address,
        )
        cls.child = Child.objects.create(
            first_name="prénom",
            last_name="Nom",
            birth_date="2020-12-20",
            vaccine_next_due_date="2020-12-20",
            cc_facility=cls.cc_facility,
        )
        cls.family_link = Family_link.objects.create(
            link_type="mère",
            retrieval_auth=True,
            emergency_contact_person=True,
            child=cls.child,
            relative=cls.family_member,
        )
        cls.child.relative.add(cls.family_member)

    def test_str(self):
        self.assertEqual(str(self.family_link), self.family_link.link_type)

    def test_child_name_label(self):
        field_label = self.family_link._meta.get_field("child").verbose_name
        self.assertEqual(field_label, "Enfant")

    def test_relative_label(self):
        field_label = self.family_link._meta.get_field("relative").verbose_name
        self.assertEqual(field_label, "Membre Familial")

    def test_link_type_label(self):
        field_label = self.family_link._meta.get_field(
            "link_type"
        ).verbose_name
        self.assertEqual(field_label, "Lien Familial")

    def test_retrieval_auth_label(self):
        field_label = self.family_link._meta.get_field(
            "retrieval_auth"
        ).verbose_name
        self.assertEqual(field_label, "Autorisation de Prise en Charge")

    def test_emergency_contact_person_label(self):
        field_label = self.family_link._meta.get_field(
            "emergency_contact_person"
        ).verbose_name
        self.assertEqual(field_label, "Contact en cas d'urgence")


class DailyFact_test(TestCase):
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
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
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
        cls.employee = Employee.objects.create(
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
        cls.daily_fact = DailyFact.objects.create(
            comment="bonne journée",
            child=cls.child,
            employee=cls.employee,
        )

    def test_str(self):
        eur_date = "{0}-{1}-{2}".format(
            self.daily_fact.time_stamp.day,
            self.daily_fact.time_stamp.month,
            self.daily_fact.time_stamp.year,
        )
        self.assertEqual(
            str(self.daily_fact),
            eur_date
            + ", "
            + str(self.daily_fact.child)
            + " écrite par "
            + str(self.daily_fact.employee),
        )

    def test_child_name_label(self):
        field_label = self.daily_fact._meta.get_field("child").verbose_name
        self.assertEqual(field_label, "Enfant")

    def test_employee_label(self):
        field_label = self.daily_fact._meta.get_field("employee").verbose_name
        self.assertEqual(field_label, "Employé")

    def test_time_stamp_type_label(self):
        field_label = self.daily_fact._meta.get_field(
            "time_stamp"
        ).verbose_name
        self.assertEqual(field_label, "Horodatage")

    def test_comment_auth_label(self):
        field_label = self.daily_fact._meta.get_field("comment").verbose_name
        self.assertEqual(field_label, "Commentaire général")


class Sleep_test(TestCase):
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
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
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
        cls.employee = Employee.objects.create(
            first_name="prénom",
            last_name="Nom",
            password="123456789",
            username="employeprenom@hotmail.com",
            phone=13510006788,
            IdScan="/fakepath/jfoijhzefe.jpg",
            occupation="healthcare",
            employee_nr="12313",
            diploma="CPA",
            Is_manager=True,
            employee_contract="/fakepath/jfoijhzefe.jpg",
            address=cls.address,
        )
        cls.daily_fact = DailyFact.objects.create(
            comment="bonne journée",
            child=cls.child,
            employee=cls.employee,
        )
        cls.sleep = Sleep.objects.create(
            length_minutes=100,
            daily_fact=cls.daily_fact,
        )

    def test_str(self):
        self.assertEqual(
            str(self.sleep), str(self.sleep.length_minutes) + " minutes"
        )

    def test_length_minutes_label(self):
        field_label = self.sleep._meta.get_field("length_minutes").verbose_name
        self.assertEqual(field_label, "Durée en Minutes")

    def test_daily_fact_label(self):
        field_label = self.sleep._meta.get_field("daily_fact").verbose_name
        self.assertEqual(field_label, "Transmission")


class Meal_test(TestCase):
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
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
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
        cls.employee = Employee.objects.create(
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
        cls.daily_fact = DailyFact.objects.create(
            comment="bonne journée",
            child=cls.child,
            employee=cls.employee,
        )
        cls.meal = Meal.objects.create(
            starter_qtty_gr=100,
            main_course_qtty_gr=100,
            desert_qtty_gr=100,
            daily_fact=cls.daily_fact,
        )

    def test_str(self):
        self.assertEqual(
            str(self.meal),
            "Entrée : {0}gr. Plat Principal : {1}gr. Déssert : {2}gr.".format(
                self.meal.starter_qtty_gr,
                self.meal.main_course_qtty_gr,
                self.meal.desert_qtty_gr,
            ),
        )

    def test_starter_qtty_gr_label(self):
        field_label = self.meal._meta.get_field("starter_qtty_gr").verbose_name
        self.assertEqual(field_label, "Quantité Entrée mangée en gr")

    def test_main_course_qtty_gr_label(self):
        field_label = self.meal._meta.get_field(
            "main_course_qtty_gr"
        ).verbose_name
        self.assertEqual(
            field_label, "Quantité Plat de résistance mangée en gr"
        )

    def test_desert_qtty_gr_qtty_gr_label(self):
        field_label = self.meal._meta.get_field("desert_qtty_gr").verbose_name
        self.assertEqual(field_label, "Quantité Déssert mangée en gr")

    def test_daily_fact_qtty_gr_label(self):
        field_label = self.meal._meta.get_field("daily_fact").verbose_name
        self.assertEqual(field_label, "Transmission")


class FeedingBottle_test(TestCase):
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
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
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
        cls.employee = Employee.objects.create(
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
        cls.daily_fact = DailyFact.objects.create(
            comment="bonne journée",
            child=cls.child,
            employee=cls.employee,
        )
        cls.feeding_bottle = FeedingBottle.objects.create(
            prepared_qtty_ml=100,
            drank_qtty_ml=100,
            daily_fact=cls.daily_fact,
        )

    def test_str(self):
        self.assertEqual(
            str(self.feeding_bottle),
            str(self.feeding_bottle.drank_qtty_ml) + "ml.",
        )

    def test_prepared_qtty_ml_qtty_gr_label(self):
        field_label = self.feeding_bottle._meta.get_field(
            "prepared_qtty_ml"
        ).verbose_name
        self.assertEqual(field_label, "Quantité Préparée ml")

    def test_drank_qtty_ml_label(self):
        field_label = self.feeding_bottle._meta.get_field(
            "drank_qtty_ml"
        ).verbose_name
        self.assertEqual(field_label, "Quantité Bue ml")

    def test_daily_fact_qtty_gr_label(self):
        field_label = self.feeding_bottle._meta.get_field(
            "daily_fact"
        ).verbose_name
        self.assertEqual(field_label, "Transmission")


class Activity_test(TestCase):
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
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
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
        cls.employee = Employee.objects.create(
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
        cls.daily_fact = DailyFact.objects.create(
            comment="bonne journée",
            child=cls.child,
            employee=cls.employee,
        )
        cls.activity = Activity.objects.create(
            activity_type="MF",
            period="AM",
            daily_fact=cls.daily_fact,
        )

    def test_str(self):
        self.assertEqual(
            str(self.activity),
            self.activity.period + " : " + "Motricité Fine" + ".",
        )

    def test_activity_type_label(self):
        field_label = self.activity._meta.get_field(
            "activity_type"
        ).verbose_name
        self.assertEqual(field_label, "Type d'Activité")

    def test_period_label(self):
        field_label = self.activity._meta.get_field("period").verbose_name
        self.assertEqual(field_label, "Période")

    def test_daily_fact_qtty_gr_label(self):
        field_label = self.activity._meta.get_field("daily_fact").verbose_name
        self.assertEqual(field_label, "Transmission")


class MedicalEvent_test(TestCase):
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
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
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
        cls.employee = Employee.objects.create(
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
        cls.daily_fact = DailyFact.objects.create(
            comment="bonne journée",
            child=cls.child,
            employee=cls.employee,
        )
        cls.medical_event = MedicalEvent.objects.create(
            description="comment",
            body_temp_deg_C=38,
            given_paracetamol_qtty_mg=100,
            paracetamol_given_time="10:00",
            daily_fact=cls.daily_fact,
        )

    def test_str(self):
        self.assertEqual(
            str(self.medical_event),
            "{0}. Température : {1} °C. Quantité de paracétamol donnée : {2} mg. à {3}H.".format(
                self.medical_event.description,
                self.medical_event.body_temp_deg_C,
                self.medical_event.given_paracetamol_qtty_mg,
                self.medical_event.paracetamol_given_time,
            ),
        )

    def test_description_label(self):
        field_label = self.medical_event._meta.get_field(
            "description"
        ).verbose_name
        self.assertEqual(field_label, "Description")

    def test_body_temp_deg_C_label(self):
        field_label = self.medical_event._meta.get_field(
            "body_temp_deg_C"
        ).verbose_name
        self.assertEqual(field_label, "Température en °C")

    def test_given_paracetamol_qtty_mg_label(self):
        field_label = self.medical_event._meta.get_field(
            "given_paracetamol_qtty_mg"
        ).verbose_name
        self.assertEqual(field_label, "Paracétamol donné en mg")

    def test_paracetamol_given_time_label(self):
        field_label = self.medical_event._meta.get_field(
            "paracetamol_given_time"
        ).verbose_name
        self.assertEqual(field_label, "Heure d'administration")

    def test_daily_fact_label(self):
        field_label = self.medical_event._meta.get_field(
            "daily_fact"
        ).verbose_name
        self.assertEqual(field_label, "Transmission")


class Message_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            place_type="rue",
            number=12,
            place_name="bellevue",
            city_name="toulouse",
            postal_code=31300,
        )
        cls.cc_facility = Child_care_facility.objects.create(
            name="les Pitchounous",
            max_child_number="12",
            type_of_facility="MAM",
            status="A",
            phone="013511225588",
            email="contact@mamlespichounous.fr",
            address=cls.address,
        )
        cls.message = Message.objects.create(
            title="titre",
            content="content",
            cc_facility=cls.cc_facility,
        )

    def test_str(self):
        self.assertEqual(str(self.message), self.message.title)

    def test_title_label(self):
        field_label = self.message._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "Titre")

    def test_time_stamp_label(self):
        field_label = self.message._meta.get_field("time_stamp").verbose_name
        self.assertEqual(field_label, "Horodatage")

    def test_content_label(self):
        field_label = self.message._meta.get_field("content").verbose_name
        self.assertEqual(field_label, "Contenu")

    def test_cc_facility_label(self):
        field_label = self.message._meta.get_field("cc_facility").verbose_name
        self.assertEqual(field_label, "Structure")
