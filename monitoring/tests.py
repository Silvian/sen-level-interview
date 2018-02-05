from unittest.mock import patch

import factory
from django.conf import settings
from django.core.files import File
from django.test import TestCase
from django.utils import timezone

from factory.django import DjangoModelFactory

from monitoring.models import CSVUpload, Login


class CSVUploadFactory(DjangoModelFactory):
    """Factory for CSV Upload"""

    csv = File(open(settings.BASE_DIR + '/data/logins.csv', 'r'))

    class Meta:
        model = CSVUpload


class LoginFactory(DjangoModelFactory):
    """Factory for Login model."""

    server_name = factory.Faker("domain_word")
    server_ip = factory.Faker("ipv4")
    username = factory.Faker("name")
    full_name = factory.Faker("name")
    contact_email = factory.Faker("email")
    contact_number = factory.Faker("phone_number")
    login_time = factory.Faker("date_time_this_year")

    class Meta:
        model = Login


class CSVUploadTestCase(TestCase):
    """Test the CSV Upload model test case."""

    def setUp(self):
        self.csv = CSVUploadFactory()

    def test_csv_upload_model_date_is_now(self):
        """Test that csv upload model created date is now."""
        date_now = timezone.now().date()

        self.assertEquals(self.csv.date.date(), date_now)

    @patch('monitoring.tasks.process_csv_task.delay')
    def test_process_csv_task_is_called(self, process_mock):
        """Test that process upload file is called."""
        new_csv = CSVUploadFactory()

        self.assertIsNotNone(new_csv)
        process_mock.assert_called_once_with(new_csv.pk)


class LoginTestCase(TestCase):
    """Test the Login model test case."""

    def setUp(self):
        self.login = LoginFactory()

    def test_login_valid_fields(self):
        """Test that all fields are validated."""
        self.assertIsNotNone(self.login.server_name)
        self.assertIsNotNone(self.login.server_ip)
        self.assertIsNotNone(self.login.username)
        self.assertIsNotNone(self.login.contact_email)
        self.assertIsNotNone(self.login.contact_number)
        self.assertIsNotNone(self.login.login_time)

    def test_login_string_function(self):
        """Test the string function returns correct name:"""
        self.assertEquals(
            str(self.login),
            "Logged on {server_name} by {username} at {login_time}".format(
                server_name=self.login.server_name,
                username=self.login.username,
                login_time=self.login.login_time,
            )
        )

# TODO: Tests are incomplete! Functional tests must be created here
# as well as tests specific to process csv task
