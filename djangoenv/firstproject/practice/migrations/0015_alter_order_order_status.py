# Generated by Django 5.0 on 2024-02-11 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0014_fooditem_food_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Order_Status',
            field=models.CharField(default='Pending', max_length=10, verbose_name='Order Status'),
        ),
    ]