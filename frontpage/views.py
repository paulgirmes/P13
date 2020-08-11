from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Child_care_facility, New
from settings import STRUCTURE

class HomePage(TemplateView):
    template_name = "frontpage/index.html"
    cc_facility = Child_care_facility.objects.get(name__icontains=STRUCTURE)
    news = list(New.objects.filter(cc_facility__name=cc_facility.name).order_by("date_time"))
    extra_context = {
        "child_care_facility": cc_facility,
        "news": news[:4],
        "gg_adress" : cc_facility.address.gg_adress_format()
    }