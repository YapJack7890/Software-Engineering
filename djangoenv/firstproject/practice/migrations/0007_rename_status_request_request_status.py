# Generated by Django 5.0 on 2024-01-24 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0006_request_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='status',
            new_name='Request_Status',
        ),
    ]
