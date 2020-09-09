from django import forms
from .models import (
    DailyFact,
    Sleep,
    Meal,
    FeedingBottle,
    Activity,
    MedicalEvent,
)

SleepFormSet = forms.inlineformset_factory(
    DailyFact,
    Sleep,
    fields=("length_minutes",),
    widgets={
        "length_minutes": forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
            }
        )
    },
    extra=1,
)

MealFormSet = forms.inlineformset_factory(
    DailyFact,
    Meal,
    exclude=("daily_fact",),
    widgets={
        "starter_qtty_gr": forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
        "main_course_qtty_gr": forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
        "desert_qtty_gr": forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
    },
    extra=1,
)

FeedingBottleFormSet = forms.inlineformset_factory(
    DailyFact,
    FeedingBottle,
    exclude=("daily_fact",),
    widgets={
        "prepared_qtty_ml": forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
        "drank_qtty_ml": forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
    },
    extra=1,
)

ActivityFormSet = forms.inlineformset_factory(
    DailyFact,
    Activity,
    exclude=("daily_fact",),
    widgets={
        "activity_type": forms.Select(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
        "period": forms.Select(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
    },
    extra=1,
)
MedicalEventFormSet = forms.inlineformset_factory(
    DailyFact,
    MedicalEvent,
    exclude=("daily_fact",),
    widgets={
        "description": forms.Textarea(
            attrs={
                "class": "form-control form-control-user",
                "cols": 40,
                "rows": 5,
                "placeholder": "Votre commentaire (OBLIGATOIRE)",
            }
        ),
        "body_temp_deg_C": forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
        "given_paracetamol_qtty_mg": forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
        "paracetamol_given_time": forms.TimeInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ),
    },
    extra=1,
)


class DailyFactForm(forms.ModelForm):
    class Meta:
        model = DailyFact
        fields = ["child", "comment", "employee"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "cols": 40,
                    "rows": 5,
                    "class": "form-control form-control-user",
                    "placeholder": "Votre commentaire (OBLIGATOIRE)",
                }
            ),
        }
