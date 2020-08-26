from django import forms
from .models import DailyFact, Sleep, Meal, FeedingBottle, Activity, MedicalEvent
from django.conf import settings

SleepFormSet = forms.inlineformset_factory(
    DailyFact, Sleep, fields=("length_minutes",),
    widgets={'length_minutes': forms.NumberInput(
        attrs={
            'class': "form-control form-control-user",
        })},
    extra=1,
)

MealFormSet = forms.inlineformset_factory(
    DailyFact, Meal, exclude=("daily_fact",),
    widgets={'starter_qtty_gr': forms.NumberInput(attrs={
                'class': "form-control form-control-user",
            }),
            'main_course_qtty_gr': forms.NumberInput(attrs={
                'class': "form-control form-control-user",
            }),
            'desert_qtty_gr': forms.NumberInput(attrs={
                'class': "form-control form-control-user",
            }),
        },
    extra=1,
)

FeedingBottleFormSet = forms.inlineformset_factory(
    DailyFact, FeedingBottle, exclude=("daily_fact",),
    widgets={'prepared_qtty_ml': forms.NumberInput(attrs={
                'class': "form-control form-control-user",
            }),
            'drank_qtty_ml': forms.NumberInput(attrs={
                'class': "form-control form-control-user",
            }),
        },
    extra=1,
)

ActivityFormSet = forms.inlineformset_factory(
    DailyFact, Activity, exclude=("daily_fact",),
    widgets={'activity_type': forms.Select(attrs={
                'class': "form-control form-control-user",
            }),
            'period': forms.Select(attrs={
                'class': "form-control form-control-user",
            }),
        },
    extra=1,
)
MedicalEventFormSet = forms.inlineformset_factory(
    DailyFact, MedicalEvent, exclude=("daily_fact",),
    widgets={'description': forms.Textarea(attrs={
                'class': "form-control form-control-user",
                'cols': 40, 'rows': 5,
                "placeholder": "Votre commentaire (OBLIGATOIRE)"
            }),
            'body_temp_deg_C': forms.NumberInput(attrs={
                'class': "form-control form-control-user",
            }),
            'given_paracetamol_qtty_mg': forms.NumberInput(attrs={
                'class': "form-control form-control-user",
            }),
            'paracetamol_given_time': forms.TimeInput (attrs={
                'class': "form-control form-control-user",
            }),
        },
    extra=1,
)

class DailyFactForm(forms.ModelForm):
    class Meta:
        model = DailyFact
        fields = ["child", "comment", "employee"]
        widgets = {
            'comment': forms.Textarea(attrs={
                'cols': 40, 'rows': 5,
                'class': "form-control form-control-user",
                "placeholder": "Votre commentaire"
            }),
        }


# class _DailyFactForm(forms.ModelForm):
#     sleep_length_minutes = forms.IntegerField(
#         max_value=600,
#         min_value=0,
#         required=False,
#         help_text='Durée en Minutes',
#         label="Sieste",
#     )
#     meal_starter_qtty_gr = forms.IntegerField(
#         max_value=1000,
#         min_value=0,
#         required=False,
#         help_text="Quantité Entrée mangée en gr",
#         label="Entrée",
#     )
#     meal_main_course_qtty_gr = forms.IntegerField(
#         max_value=1000,
#         min_value=0,
#         required=False,
#         help_text="Quantité Plat de résistance mangée en gr",
#         label="Plat de résistance",
#     )
#     meal_desert_qtty_gr = forms.IntegerField(
#         max_value=1000,
#         min_value=0,
#         required=False,
#         help_text="Quantité Déssert mangée en gr",
#         label="Déssert",
#     )
#     feeding_b_prepared_qtty_ml = forms.IntegerField(
#         max_value=1000,
#         min_value=0,
#         required=False,
#         help_text="Quantité Préparée ml",
#         label="biberon",
#     )
#     feeding_b_drank_qtty_ml = forms.IntegerField(
#         max_value=1000,
#         min_value=0,
#         required=False,
#         help_text="Quantité Bue ml",
#         label="biberon",
#     )

#     choices = list(settings.ACTIVITIES_CHOICES)
#     choices.insert(0,("---","---"))
#     activity_activity_type = forms.ChoiceField(
#         required=False,
#         label="Type d'Activité",
#         choices = choices,
#     )
#     activity_period = forms.TypedChoiceField(
#         required=False,
#         label="Période de l'activité",
        
#         choices= [
#             ("---","---"),
#             ("AM","Matin"),
#             ("PM", "Après-Midi"),
#         ]
#     )
#     medicalEvent_description = forms.CharField(
#         required=False,
#         help_text="maximum 200 carartères",
#         label="description",
#         widget = forms.Textarea(attrs={
#                 'cols': 40, 'rows': 5,
#                 'class': "form-control form-control-user",
#             }),
#     )
#     medicalEvent_body_temp_deg_C = forms.DecimalField(
#         max_value=50,
#         min_value=0,
#         required=False,
#         help_text="température en °C XX,X",
#         label="température",
#         max_digits=3,
#         decimal_places=1,
#     )
#     medicalEvent_given_paracetamol_qtty_mg = forms.IntegerField(
#         max_value=2000,
#         min_value=0,
#         required=False,
#         help_text="Paracétamol donné en mg",
#         label="Paracétamol",
#     )

#     class Meta:
#         model = DailyFact
#         fields = ["comment"]
#         widgets = {
#             'comment': forms.Textarea(attrs={
#                 'cols': 40, 'rows': 5,
#                 'class': "form-control form-control-user",
#             }),
#         }


