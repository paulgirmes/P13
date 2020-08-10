from django.shortcuts import render
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "frontpage/index.html"
    extra_context = {"structure_name": "Les Pitchounous"}
