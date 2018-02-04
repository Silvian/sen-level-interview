"""Monitoring object models."""
from time import time

from django.db import models
from django.utils import timezone


def get_upload_file_name(instance, filename):
    """Process upload file name."""
    return "upload/{}_{}".format(str(time()).replace('.', '_'), filename)


class CSVUpload(models.Model):
    """CSV Upload object model class."""
    csv = models.FileField(
        upload_to=get_upload_file_name,
    )
    date = models.DateTimeField(
        default=timezone.now
    )

    def publish(self):
        """Call save method."""
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return self.csv.name


class Login(models.Model):
    """Login Data object model class."""

    server_name = models.CharField(
        max_length=255,
        blank=True,
    )
    server_ip = models.CharField(
        max_length=20,
    )
    username = models.CharField(
        max_length=500,
    )
    full_name = models.CharField(
        max_length=500,
    )
    contact_email = models.EmailField(
        blank=True,
    )
    contact_number = models.CharField(
        max_length=255,
        blank=True,
    )
    login_time = models.DateTimeField(

    )

    def publish(self):
        """Call save method."""
        self.save()

    def __str__(self):
        return "Logged on {server_name} by {username} at {login_time}".format(
            server_name=self.server_name,
            username=self.username,
            login_time=self.login_time,
        )

