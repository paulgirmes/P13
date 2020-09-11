"""
integration tests for day_to_day views
"""
import datetime
from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from frontpage.models import Child_care_facility, User
from auth_access_admin.models import Address, Employee, FamilyMember
from day_to_day.models import (
    Message,
    Child,
    DailyFact,
    Sleep,
    Meal,
    Activity,
    MedicalEvent,
    FeedingBottle,
)


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

    def test_post_request_comment_only_is_validated(self):
        self.assertTrue(
            self.client.login(
                username="employe@hotmail.com", password="123456789"
            )
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmission_add",
                args=[self.child.pk],
                current_app="d_to_d",
            ),
            data={
                "comment": "abc",
                "sleep_set-TOTAL_FORMS": "1",
                "sleep_set-INITIAL_FORMS": "0",
                "sleep_set-MIN_NUM_FORMS": "0",
                "sleep_set-MAX_NUM_FORMS": "1000",
                "sleep_set-0-length_minutes": "",
                "sleep_set-0-id": "",
                "sleep_set-0-daily_fact": "",
                "meal_set-TOTAL_FORMS": "1",
                "meal_set-INITIAL_FORMS": "0",
                "feedingbottle_set-TOTAL_FORMS": "1",
                "meal_set-INITIAL_FORMS": "0",
                "meal_set-MIN_NUM_FORMS": "0",
                "meal_set-MAX_NUM_FORMS": "1000",
                "meal_set-0-starter_qtty_gr": "",
                "meal_set-0-main_course_qtty_gr": "",
                "meal_set-0-desert_qtty_gr": "",
                "meal_set-0-id": "",
                "meal_set-0-daily_fact": "",
                "activity_set-TOTAL_FORMS": "1",
                "activity_set-INITIAL_FORMS": "0",
                "activity_set-MIN_NUM_FORMS": "0",
                "activity_set-MAX_NUM_FORMS": "1000",
                "activity_set-0-activity_type": "",
                "activity_set-0-period": "",
                "activity_set-0-id": "",
                "activity_set-0-daily_fact": "",
                "feedingbottle_set-INITIAL_FORMS": "0",
                "feedingbottle_set-MIN_NUM_FORMS": "0",
                "feedingbottle_set-MAX_NUM_FORMS": "1000",
                "feedingbottle_set-0-prepared_qtty_ml": "",
                "feedingbottle_set-0-drank_qtty_ml": "",
                "feedingbottle_set-0-id": "",
                "feedingbottle_set-0-daily_fact": "",
                "medicalevent_set-TOTAL_FORMS": "1",
                "medicalevent_set-INITIAL_FORMS": "0",
                "medicalevent_set-MIN_NUM_FORMS": "0",
                "medicalevent_set-MAX_NUM_FORMS": "1000",
            },
        )
        self.assertRedirects(
            response,
            expected_url=reverse(
                "d_to_d:Child_transmissions",
                args=(self.child.pk, True),
                current_app="d_to_d",
            ),
        )
        self.assertEqual(
            DailyFact.objects.get(child=self.child).comment, "abc"
        )

    def test_post_request_comment_all_valid(self):
        self.assertTrue(
            self.client.login(
                username="employe@hotmail.com", password="123456789"
            )
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmission_add",
                args=[self.child.pk],
                current_app="d_to_d",
            ),
            data={
                "comment": "aaaa",
                "sleep_set-TOTAL_FORMS": "1",
                "sleep_set-INITIAL_FORMS": "0",
                "sleep_set-MIN_NUM_FORMS": "0",
                "sleep_set-MAX_NUM_FORMS": "1000",
                "sleep_set-0-length_minutes": "60",
                "sleep_set-0-id": "",
                "sleep_set-0-daily_fact": "",
                "meal_set-TOTAL_FORMS": "1",
                "meal_set-INITIAL_FORMS": "0",
                "feedingbottle_set-TOTAL_FORMS": "1",
                "meal_set-INITIAL_FORMS": "0",
                "meal_set-MIN_NUM_FORMS": "0",
                "meal_set-MAX_NUM_FORMS": "1000",
                "meal_set-0-starter_qtty_gr": "60",
                "meal_set-0-main_course_qtty_gr": "60",
                "meal_set-0-desert_qtty_gr": "60",
                "meal_set-0-id": "",
                "meal_set-0-daily_fact": "",
                "activity_set-TOTAL_FORMS": "1",
                "activity_set-INITIAL_FORMS": "0",
                "activity_set-MIN_NUM_FORMS": "0",
                "activity_set-MAX_NUM_FORMS": "1000",
                "activity_set-0-activity_type": "MF",
                "activity_set-0-period": "AM",
                "activity_set-0-id": "",
                "activity_set-0-daily_fact": "",
                "feedingbottle_set-INITIAL_FORMS": "0",
                "feedingbottle_set-MIN_NUM_FORMS": "0",
                "feedingbottle_set-MAX_NUM_FORMS": "1000",
                "feedingbottle_set-0-prepared_qtty_ml": "60",
                "feedingbottle_set-0-drank_qtty_ml": "60",
                "feedingbottle_set-0-id": "",
                "feedingbottle_set-0-daily_fact": "",
                "medicalevent_set-TOTAL_FORMS": "1",
                "medicalevent_set-INITIAL_FORMS": "0",
                "medicalevent_set-MIN_NUM_FORMS": "0",
                "medicalevent_set-MAX_NUM_FORMS": "1000",
                "medicalevent_set-0-description": "azbd",
                "medicalevent_set-0-body_temp_deg_C": "35",
                "medicalevent_set-0-given_paracetamol_qtty_mg": "100",
                "medicalevent_set-0-paracetamol_given_time": "10:00",
                "medicalevent_set-0-id": "",
                "medicalevent_set-0-daily_fact": "",
            },
        )
        self.assertRedirects(
            response,
            expected_url=reverse(
                "d_to_d:Child_transmissions",
                args=(self.child.pk, True),
                current_app="d_to_d",
            ),
        )
        self.assertEqual(
            DailyFact.objects.get(child=self.child).comment, "aaaa"
        )
        self.assertTrue(
            Sleep.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            )
        )
        self.assertTrue(
            Meal.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            )
        )
        self.assertTrue(
            Activity.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            )
        )
        self.assertTrue(
            FeedingBottle.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            )
        )
        self.assertTrue(
            MedicalEvent.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            )
        )


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
        cls.trans = DailyFact.objects.create(
            employee=cls.employee, child=cls.child, comment="abc"
        )

    def test_post_request_is_valid_comment(self):
        self.assertTrue(
            self.client.login(
                username="employe@hotmail.com", password="123456789"
            )
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "comment": "aaaa",
            },
        )
        self.assertRedirects(
            response,
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
        )
        self.assertIsInstance(DailyFact.objects.get(comment="aaaa"), DailyFact)

    def test_post_request_is_valid_formset_comment(self):
        self.assertTrue(
            self.client.login(
                username="employe@hotmail.com", password="123456789"
            )
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "sleep_set-TOTAL_FORMS": "1",
                "sleep_set-INITIAL_FORMS": "0",
                "sleep_set-MIN_NUM_FORMS": "0",
                "sleep_set-MAX_NUM_FORMS": "1000",
                "sleep_set-0-length_minutes": "60",
                "sleep_set-0-id": "",
                "sleep_set-0-daily_fact": "",
            },
        )
        self.assertRedirects(
            response,
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
        )
        self.assertEqual(
            Sleep.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).length_minutes,
            60,
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "meal_set-TOTAL_FORMS": "1",
                "meal_set-INITIAL_FORMS": "0",
                "meal_set-INITIAL_FORMS": "0",
                "meal_set-MIN_NUM_FORMS": "0",
                "meal_set-MAX_NUM_FORMS": "1000",
                "meal_set-0-starter_qtty_gr": "60",
                "meal_set-0-main_course_qtty_gr": "60",
                "meal_set-0-desert_qtty_gr": "60",
                "meal_set-0-id": "",
                "meal_set-0-daily_fact": "",
            },
        )
        self.assertRedirects(
            response,
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
        )
        self.assertEqual(
            Meal.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).starter_qtty_gr,
            60,
        )
        self.assertEqual(
            Meal.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).main_course_qtty_gr,
            60,
        )
        self.assertEqual(
            Meal.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).desert_qtty_gr,
            60,
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "activity_set-TOTAL_FORMS": "1",
                "activity_set-INITIAL_FORMS": "0",
                "activity_set-MIN_NUM_FORMS": "0",
                "activity_set-MAX_NUM_FORMS": "1000",
                "activity_set-0-activity_type": "MF",
                "activity_set-0-period": "AM",
                "activity_set-0-id": "",
                "activity_set-0-daily_fact": "",
            },
        )
        self.assertEqual(
            Activity.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).activity_type,
            "MF",
        )
        self.assertEqual(
            Activity.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).period,
            "AM",
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "feedingbottle_set-TOTAL_FORMS": "1",
                "feedingbottle_set-INITIAL_FORMS": "0",
                "feedingbottle_set-MIN_NUM_FORMS": "0",
                "feedingbottle_set-MAX_NUM_FORMS": "1000",
                "feedingbottle_set-0-prepared_qtty_ml": "60",
                "feedingbottle_set-0-drank_qtty_ml": "60",
                "feedingbottle_set-0-id": "",
                "feedingbottle_set-0-daily_fact": "",
            },
        )
        self.assertEqual(
            FeedingBottle.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).prepared_qtty_ml,
            60,
        )
        self.assertEqual(
            FeedingBottle.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).drank_qtty_ml,
            60,
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "medicalevent_set-TOTAL_FORMS": "1",
                "medicalevent_set-INITIAL_FORMS": "0",
                "medicalevent_set-MIN_NUM_FORMS": "0",
                "medicalevent_set-MAX_NUM_FORMS": "1000",
                "medicalevent_set-0-description": "azbd",
                "medicalevent_set-0-body_temp_deg_C": "35",
                "medicalevent_set-0-given_paracetamol_qtty_mg": "100",
                "medicalevent_set-0-paracetamol_given_time": "10:00",
                "medicalevent_set-0-id": "",
                "medicalevent_set-0-daily_fact": "",
            },
        )
        self.assertEqual(
            MedicalEvent.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).description,
            "azbd",
        )
        self.assertEqual(
            MedicalEvent.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).body_temp_deg_C,
            35,
        )
        self.assertEqual(
            MedicalEvent.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).given_paracetamol_qtty_mg,
            100,
        )
        self.assertEqual(
            MedicalEvent.objects.get(
                daily_fact=DailyFact.objects.get(child=self.child)
            ).paracetamol_given_time,
            datetime.time(10, 0),
        )

    def test_post_request_is_not_valid_formset(self):
        self.assertTrue(
            self.client.login(
                username="employe@hotmail.com", password="123456789"
            )
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "medicalevent_set-TOTAL_FORMS": "1",
                "medicalevent_set-INITIAL_FORMS": "0",
                "medicalevent_set-MIN_NUM_FORMS": "0",
                "medicalevent_set-MAX_NUM_FORMS": "1000",
                "medicalevent_set-0-description": "azbd",
                "medicalevent_set-0-body_temp_deg_C": "AB",
                "medicalevent_set-0-given_paracetamol_qtty_mg": "100",
                "medicalevent_set-0-paracetamol_given_time": "10:00",
                "medicalevent_set-0-id": "",
                "medicalevent_set-0-daily_fact": "",
            },
        )
        with self.assertRaises(ObjectDoesNotExist):
            MedicalEvent.objects.get(
                daily_fact=DailyFact.objects.get(comment="abc")
            )
        self.assertEqual(
            response.context.get("message"),
            "La modification de la donnée "
            + "Médical"
            + " n'a pas été effectuée merci de vérifier les erreurs",
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "feedingbottle_set-TOTAL_FORMS": "1",
                "feedingbottle_set-INITIAL_FORMS": "0",
                "feedingbottle_set-MIN_NUM_FORMS": "0",
                "feedingbottle_set-MAX_NUM_FORMS": "1000",
                "feedingbottle_set-0-prepared_qtty_ml": "AB",
                "feedingbottle_set-0-drank_qtty_ml": "60",
                "feedingbottle_set-0-id": "",
                "feedingbottle_set-0-daily_fact": "",
            },
        )
        with self.assertRaises(ObjectDoesNotExist):
            FeedingBottle.objects.get(
                daily_fact=DailyFact.objects.get(comment="abc")
            )
        self.assertEqual(
            response.context.get("message"),
            "La modification de la donnée "
            + "Biberons"
            + " n'a pas été effectuée merci de vérifier les erreurs",
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "meal_set-TOTAL_FORMS": "1",
                "meal_set-INITIAL_FORMS": "0",
                "meal_set-INITIAL_FORMS": "0",
                "meal_set-MIN_NUM_FORMS": "0",
                "meal_set-MAX_NUM_FORMS": "1000",
                "meal_set-0-starter_qtty_gr": "AB",
                "meal_set-0-main_course_qtty_gr": "60",
                "meal_set-0-desert_qtty_gr": "60",
                "meal_set-0-id": "",
                "meal_set-0-daily_fact": "",
            },
        )
        with self.assertRaises(ObjectDoesNotExist):
            Meal.objects.get(daily_fact=DailyFact.objects.get(comment="abc"))
        self.assertEqual(
            response.context.get("message"),
            "La modification de la donnée "
            + "Repas"
            + " n'a pas été effectuée merci de vérifier les erreurs",
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "activity_set-TOTAL_FORMS": "1",
                "activity_set-INITIAL_FORMS": "0",
                "activity_set-MIN_NUM_FORMS": "0",
                "activity_set-MAX_NUM_FORMS": "1000",
                "activity_set-0-activity_type": "MF",
                "activity_set-0-period": "10",
                "activity_set-0-id": "",
                "activity_set-0-daily_fact": "",
            },
        )
        with self.assertRaises(ObjectDoesNotExist):
            Activity.objects.get(
                daily_fact=DailyFact.objects.get(comment="abc")
            )
        self.assertEqual(
            response.context.get("message"),
            "La modification de la donnée "
            + "Activités"
            + " n'a pas été effectuée merci de vérifier les erreurs",
        )
        response = self.client.post(
            reverse(
                "d_to_d:transmissions_change",
                args=[self.trans.pk],
                current_app="d_to_d",
            ),
            data={
                "sleep_set-TOTAL_FORMS": "1",
                "sleep_set-INITIAL_FORMS": "0",
                "sleep_set-MIN_NUM_FORMS": "0",
                "sleep_set-MAX_NUM_FORMS": "1000",
                "sleep_set-0-length_minutes": "AB",
                "sleep_set-0-id": "",
                "sleep_set-0-daily_fact": "",
            },
        )
        with self.assertRaises(ObjectDoesNotExist):
            Sleep.objects.get(daily_fact=DailyFact.objects.get(comment="abc"))
        self.assertEqual(
            response.context.get("message"),
            "La modification de la donnée "
            + "Sieste"
            + " n'a pas été effectuée merci de vérifier les erreurs",
        )
