# Generated by Django 5.0.2 on 2024-02-27 14:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_remove_calendar_catalog_page_catalogpage_calendar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogpage',
            name='calendar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.calendar'),
        ),
    ]
