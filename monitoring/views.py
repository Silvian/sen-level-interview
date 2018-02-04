"""Monitoring views."""
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Render index view."""

    template_name = "monitoring/index.html"

