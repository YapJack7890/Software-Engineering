# Generated by Django 5.0.1 on 2024-01-28 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0009_alter_request_request_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='Request_Status',
        ),
    ]
