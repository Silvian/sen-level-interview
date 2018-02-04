from django.contrib import admin

from .models import Login, CSVUpload

admin.site.register(CSVUpload)
admin.site.register(Login)
