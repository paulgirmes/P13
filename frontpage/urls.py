"""
CC_ERP URL Configuration
"""

from django.urls import path
from . import views

app_name = "frontpage"

urlpatterns = [
    path("", views.HomePage.as_view(), name="homepage"),
    path("conditions-generales/", views.Legal.as_view(), name="legal"),
]
