"""CC_ERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
