# Generated by Django 5.0 on 2024-01-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0005_remove_order_food_order_food_items_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.CharField(default='Pending', max_length=10, verbose_name='Status'),
        ),
    ]
