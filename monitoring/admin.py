from django.contrib import admin

from .models import Login, CSVUpload


@admin.register(CSVUpload)
class CSVUploadAdmin(admin.ModelAdmin):
    """CSV Upload admin."""

    list_display = ('csv', 'date',)

    list_filter = ('date',)


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    """Login admin."""

    list_display = (
        'server_ip',
        'server_name',
        'username',
        'full_name',
        'contact_email',
        'contact_number',
        'login_time',
    )

    search_fields = (
        'server_name',
        'server_id',
        'user_name',
        'full_name',
    )

    list_filter = ('login_time',)
