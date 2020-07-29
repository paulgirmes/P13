from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "frontpage/index.html"
    extra_context = {"coucou": "coucou"}
