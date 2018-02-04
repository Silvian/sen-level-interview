"""Monitoring views."""
from django.http import HttpResponseRedirect
from django.views import generic

from .models import CSVUpload
from .forms import CSVUploadForm


class HomeView(generic.FormView, generic.TemplateView):
    """Render index view."""

    model = CSVUpload
    template_name = 'monitoring/index.html'
    form_class = CSVUploadForm
    success_url = '/'
    context_object_name = 'csv'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/')

