"""Monitoring forms."""
from django import forms

from .models import CSVUpload


class CSVUploadForm(forms.ModelForm):
    """CSV Upload model form."""

    def __init__(self, *args, **kwargs):
        super(CSVUploadForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CSVUpload
        fields = ('csv',)
