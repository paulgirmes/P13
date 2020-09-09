"""
unit tests for day_to_day forms
"""

from django.test import SimpleTestCase
from day_to_day.forms import (
    SleepFormSet,
    MealFormSet,
    FeedingBottleFormSet,
    ActivityFormSet,
    MedicalEventFormSet,
    DailyFactForm,
)
from day_to_day.models import (
    DailyFact,
    Sleep,
    Meal,
    Activity,
    FeedingBottle,
    MedicalEvent,
)


class SleepFormSetTest(SimpleTestCase):
    def test_model(self):
        form = SleepFormSet()
        self.assertEqual(
            form.model,
            Sleep,
        )

    def test_fields(self):
        form = SleepFormSet()
        self.assertTrue(form.empty_form.fields.get("length_minutes"))

    def test_widget_extra(self):
        form = SleepFormSet().empty_form.fields.get("length_minutes")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/number.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEqual(
            SleepFormSet().extra,
            1,
        )


class MealFormSetTest(SimpleTestCase):
    def test_model(self):
        form = MealFormSet()
        self.assertEqual(
            form.model,
            Meal,
        )

    def test_fields(self):
        form = MealFormSet()
        self.assertTrue(form.empty_form.fields.get("starter_qtty_gr"))
        self.assertTrue(form.empty_form.fields.get("main_course_qtty_gr"))
        self.assertTrue(form.empty_form.fields.get("desert_qtty_gr"))

    def test_widget_extra(self):
        form = MealFormSet().empty_form.fields.get("starter_qtty_gr")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/number.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEqual(
            MealFormSet().extra,
            1,
        )
        form = MealFormSet().empty_form.fields.get("main_course_qtty_gr")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/number.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEqual(
            MealFormSet().extra,
            1,
        )
        form = MealFormSet().empty_form.fields.get("desert_qtty_gr")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/number.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEqual(
            MealFormSet().extra,
            1,
        )


class FeedingBottleFormSetTest(SimpleTestCase):
    def test_model(self):
        form = FeedingBottleFormSet()
        self.assertEqual(
            form.model,
            FeedingBottle,
        )

    def test_fields(self):
        form = FeedingBottleFormSet()
        self.assertTrue(form.empty_form.fields.get("prepared_qtty_ml"))
        self.assertTrue(form.empty_form.fields.get("drank_qtty_ml"))

    def test_widget_extra(self):
        form = FeedingBottleFormSet().empty_form.fields.get("prepared_qtty_ml")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/number.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEqual(
            FeedingBottleFormSet().extra,
            1,
        )
        form = FeedingBottleFormSet().empty_form.fields.get("drank_qtty_ml")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/number.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEqual(
            FeedingBottleFormSet().extra,
            1,
        )


class ActivityFormSetTest(SimpleTestCase):
    def test_model(self):
        form = ActivityFormSet()
        self.assertEqual(
            form.model,
            Activity,
        )

    def test_fields(self):
        form = ActivityFormSet()
        self.assertTrue(form.empty_form.fields.get("activity_type"))
        self.assertTrue(form.empty_form.fields.get("period"))

    def test_widget_extra(self):
        form = ActivityFormSet().empty_form.fields.get("activity_type")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/select.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user"},
        )
        self.assertEqual(
            ActivityFormSet().extra,
            1,
        )
        form = ActivityFormSet().empty_form.fields.get("period")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/select.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {
                "class": "form-control form-control-user",
            },
        )
        self.assertEqual(
            ActivityFormSet().extra,
            1,
        )


class MedicalEventFormSetTest(SimpleTestCase):
    def test_model(self):
        form = MedicalEventFormSet()
        self.assertEqual(
            form.model,
            MedicalEvent,
        )

    def test_fields(self):
        form = MedicalEventFormSet()
        self.assertTrue(form.empty_form.fields.get("description"))
        self.assertTrue(form.empty_form.fields.get("body_temp_deg_C"))
        self.assertTrue(
            form.empty_form.fields.get("given_paracetamol_qtty_mg")
        )
        self.assertTrue(form.empty_form.fields.get("paracetamol_given_time"))

    def test_widget_extra(self):
        form = MedicalEventFormSet().empty_form.fields.get("description")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/textarea.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {
                "cols": 40,
                "class": "form-control form-control-user",
                "placeholder": "Votre commentaire (OBLIGATOIRE)",
                "rows": 5,
                "maxlength": "200",
            },
        )
        self.assertEqual(
            MedicalEventFormSet().extra,
            1,
        )
        form = MedicalEventFormSet().empty_form.fields.get("body_temp_deg_C")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/number.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user", "step": "0.1"},
        )
        self.assertEqual(
            MedicalEventFormSet().extra,
            1,
        )
        form = MedicalEventFormSet().empty_form.fields.get(
            "given_paracetamol_qtty_mg"
        )
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/number.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEqual(
            MedicalEventFormSet().extra,
            1,
        )
        form = MedicalEventFormSet().empty_form.fields.get(
            "paracetamol_given_time"
        )
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/time.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {"class": "form-control form-control-user"},
        )
        self.assertEqual(
            MedicalEventFormSet().extra,
            1,
        )


class DailyFactFormTest(SimpleTestCase):
    def test_model(self):
        form = DailyFactForm()
        self.assertEqual(
            form.Meta.model,
            DailyFact,
        )

    def test_fields(self):
        form = DailyFactForm()
        self.assertTrue(form.fields.get("child"))
        self.assertTrue(form.fields.get("comment"))
        self.assertTrue(form.fields.get("employee"))

    def test_widget_extra(self):
        form = DailyFactForm().fields.get("comment")
        self.assertEqual(
            form.widget.template_name,
            "django/forms/widgets/textarea.html",
        )
        self.assertEqual(
            form.widget.attrs,
            {
                "cols": 40,
                "class": "form-control form-control-user",
                "placeholder": "Votre commentaire (OBLIGATOIRE)",
                "rows": 5,
                "maxlength": "200",
            },
        )
