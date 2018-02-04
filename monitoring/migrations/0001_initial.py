# Generated by Django 2.0.1 on 2018-02-04 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_name', models.CharField(blank=True, max_length=255)),
                ('server_ip', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=500)),
                ('full_name', models.CharField(max_length=500)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_number', models.CharField(blank=True, max_length=255)),
                ('login_time', models.DateTimeField()),
            ],
        ),
    ]
