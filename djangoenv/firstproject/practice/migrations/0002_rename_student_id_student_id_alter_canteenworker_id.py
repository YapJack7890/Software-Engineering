# Generated by Django 5.0 on 2024-01-16 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='Student_ID',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='canteenworker',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
