# Generated by Django 2.0.1 on 2018-02-04 17:26

from django.db import migrations, models
import django.utils.timezone
import monitoring.models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv', models.FileField(upload_to=monitoring.models.get_upload_file_name)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
