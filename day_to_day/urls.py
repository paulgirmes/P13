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
    path("employé/", views.EmployeeView.as_view(), name="employee"),
    path("employé/enfants/", views.ChildListView.as_view(), name="child_list"),
    path("employé/transmissions/", views.TransmissionsListView.as_view(), name="tr_list"),
    path("employé/enfants/<str:first_n>-<str:last_n>/", views.ChildView.as_view(), name="Child_facts"),
    path("employé/enfants/<str:first_n>-<str:last_n>/transmissions/", views.ChildTransmissionsView.as_view(), name="Child_transmissions"),
    path("employé/enfants/<str:first_n>-<str:last_n>/transmissions/ajouter/<int:id>", views.ChildTransmissionsAddView.as_view(), name="transmission_add"),
    path("employé/enfants/<str:first_n>-<str:last_n>/transmissions/modifier/<int:id>", views.ChildTransmissionsChangeView.as_view(), name="transmissions_change"),
    path("parent/", views.ParentView.as_view(), name="parent"),
]