from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Child_care_facility, New
from django.conf import settings


def page_not_found_view(request, exception=None):
    return render(request,"frontpage/_404.html",status=404)

def error_view(request, exception=None):
    return render(request, "frontpage/_500.html", status=500)

class HomePage(TemplateView):
    template_name = "frontpage/_index.html"
    try:
        cc_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
        news = list(New.objects.filter(cc_facility__name=cc_facility.name).order_by("date_time"))
        extra_context = {
            "child_care_facility": cc_facility,
            "news": news[:4],
            "gg_adress" : cc_facility.address.gg_adress_format()
        }
    except:
        extra_context = {
            "child_care_facility": None,
            "news": None,
            "gg_adress" : None,
        }

class Legal(TemplateView):
    template_name = "frontpage/_legal.html"
    try:
        cc_facility = Child_care_facility.objects.get(name=settings.STRUCTURE)
        extra_context = {
            "child_care_facility": cc_facility,
        }
    except:
        extra_context = {
            "child_care_facility": None,
        }
