"""
CC_ERP URL Configuration
"""

from django.urls import path
from . import views

app_name = "d_to_d"

urlpatterns = [
    path("employe/", views.EmployeeView.as_view(), name="employee"),
    path("employe/enfants/", views.ChildListView.as_view(), name="child_list"),
    path(
        "employe/transmissions/",
        views.EmployeeTransmissionsListView.as_view(),
        name="tr_list",
    ),
    path(
        "employe/enfants/<int:pk>/",
        views.ChildView.as_view(),
        name="Child_facts",
    ),
    path(
        "employe/enfants/<int:pk>/transmissions/<str:success>",
        views.ChildTransmissionsView.as_view(),
        name="Child_transmissions",
    ),
    path(
        "employe/enfants/<int:pk>/transmissions/ajouter/",
        views.ChildTransmissionsAddView.as_view(),
        name="transmission_add",
    ),
    path(
        "employe/transmission/modifier/<int:pk>",
        views.TransmissionsChangeView.as_view(pk="pk"),
        name="transmissions_change",
    ),
    path("parent/", views.ParentView.as_view(), name="parent"),
    path(
        "child/<int:pk>/",
        views.Child_transmissions_report.as_view(),
        name="child",
    ),
]
