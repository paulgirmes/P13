"""
unit tests for day_to_day forms
"""

from django.test import SimpleTestCase
from day_to_day.forms import (
    SleepFormSet, MealFormSet, FeedingBottleFormSet,
    ActivityFormSet, MedicalEventFormSet, DailyFactForm,
)
from day_to_day.models import (
    DailyFact, Sleep, Meal, Activity,
    FeedingBottle, MedicalEvent,
)


class SleepFormSetTest(SimpleTestCase):

    def test_model(self):
        form = SleepFormSet()
        self.assertEquals(
            form.model,
            Sleep,
            )
    
    def test_fields(self):
        form = SleepFormSet()
        self.assertTrue(
            form.empty_form.fields.get("length_minutes")
            )

    def test_widget_extra(self):
        form = SleepFormSet().empty_form.fields.get("length_minutes")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/number.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEquals(
            SleepFormSet().extra, 1,
        )


class MealFormSetTest(SimpleTestCase):

    def test_model(self):
        form = MealFormSet()
        self.assertEquals(
            form.model,
            Meal,
            )
    
    def test_fields(self):
        form = MealFormSet()
        self.assertTrue(
            form.empty_form.fields.get("starter_qtty_gr")
            )
        self.assertTrue(
            form.empty_form.fields.get("main_course_qtty_gr")
            )
        self.assertTrue(
            form.empty_form.fields.get("desert_qtty_gr")
            )

    def test_widget_extra(self):
        form = MealFormSet().empty_form.fields.get("starter_qtty_gr")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/number.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEquals(
            MealFormSet().extra, 1,
        )
        form = MealFormSet().empty_form.fields.get("main_course_qtty_gr")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/number.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEquals(
            MealFormSet().extra, 1,
        )
        form = MealFormSet().empty_form.fields.get("desert_qtty_gr")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/number.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEquals(
            MealFormSet().extra, 1,
        )


class FeedingBottleFormSetTest(SimpleTestCase):

    def test_model(self):
        form = FeedingBottleFormSet()
        self.assertEquals(
            form.model,
            FeedingBottle,
            )
    
    def test_fields(self):
        form = FeedingBottleFormSet()
        self.assertTrue(
            form.empty_form.fields.get("prepared_qtty_ml")
            )
        self.assertTrue(
            form.empty_form.fields.get("drank_qtty_ml")
            )

    def test_widget_extra(self):
        form = FeedingBottleFormSet().empty_form.fields.get("prepared_qtty_ml")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/number.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEquals(
            FeedingBottleFormSet().extra, 1,
        )
        form = FeedingBottleFormSet().empty_form.fields.get("drank_qtty_ml")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/number.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEquals(
            FeedingBottleFormSet().extra, 1,
        )


class ActivityFormSetTest(SimpleTestCase):

    def test_model(self):
        form = ActivityFormSet()
        self.assertEquals(
            form.model,
            Activity,
            )
    
    def test_fields(self):
        form = ActivityFormSet()
        self.assertTrue(
            form.empty_form.fields.get("activity_type")
            )
        self.assertTrue(
            form.empty_form.fields.get("period")
            )

    def test_widget_extra(self):
        form = ActivityFormSet().empty_form.fields.get("activity_type")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/select.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user"},
        )
        self.assertEquals(
            ActivityFormSet().extra, 1,
        )
        form = ActivityFormSet().empty_form.fields.get("period")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/select.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user",},
        )
        self.assertEquals(
            ActivityFormSet().extra, 1,
        )


class MedicalEventFormSetTest(SimpleTestCase):

    def test_model(self):
        form = MedicalEventFormSet()
        self.assertEquals(
            form.model,
            MedicalEvent,
            )
    
    def test_fields(self):
        form = MedicalEventFormSet()
        self.assertTrue(
            form.empty_form.fields.get("description")
            )
        self.assertTrue(
            form.empty_form.fields.get("body_temp_deg_C")
            )
        self.assertTrue(
            form.empty_form.fields.get("given_paracetamol_qtty_mg")
            )
        self.assertTrue(
            form.empty_form.fields.get("paracetamol_given_time")
            )

    def test_widget_extra(self):
        form = MedicalEventFormSet().empty_form.fields.get("description")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/textarea.html",
        )
        self.assertEquals(
            form.widget.attrs, 
            {
                'cols': 40,
                'class': "form-control form-control-user",
                "placeholder": "Votre commentaire (OBLIGATOIRE)",
                'rows': 5,
                'maxlength': '200',
            },
        )
        self.assertEquals(
            MedicalEventFormSet().extra, 1,
        )
        form = MedicalEventFormSet().empty_form.fields.get("body_temp_deg_C")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/number.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user", "step": "0.1"},
        )
        self.assertEquals(
            MedicalEventFormSet().extra, 1,
        )
        form = MedicalEventFormSet().empty_form.fields.get("given_paracetamol_qtty_mg")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/number.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user", "min": 0},
        )
        self.assertEquals(
            MedicalEventFormSet().extra, 1,
        )
        form = MedicalEventFormSet().empty_form.fields.get("paracetamol_given_time")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/time.html",
        )
        self.assertEquals(
            form.widget.attrs, {"class": "form-control form-control-user"},
        )
        self.assertEquals(
            MedicalEventFormSet().extra, 1,
        )
class DailyFactFormTest(SimpleTestCase):

    def test_model(self):
        form = DailyFactForm()
        self.assertEquals(
            form.Meta.model,
            DailyFact,
            )
    
    def test_fields(self):
        form = DailyFactForm()
        self.assertTrue(
            form.fields.get("child")
            )
        self.assertTrue(
            form.fields.get("comment")
            )
        self.assertTrue(
            form.fields.get("employee")
            )

    def test_widget_extra(self):
        form = DailyFactForm().fields.get("comment")
        self.assertEquals(
            form.widget.template_name, "django/forms/widgets/textarea.html",
        )
        self.assertEquals(
            form.widget.attrs, 
            {
                'cols': 40,
                'class': "form-control form-control-user",
                "placeholder": "Votre commentaire (OBLIGATOIRE)",
                'rows': 5,
                'maxlength': '200',
            },
        )