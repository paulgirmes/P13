from django.shortcuts import render
from django.views.generic import FormView


class Login_page(FormView):
    template_name = "frontpage/index.html"
    extra_context = {"coucou": "coucou"}
