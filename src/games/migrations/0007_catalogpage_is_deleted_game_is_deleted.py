# Generated by Django 5.0.2 on 2024-03-26 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_calendarblock_subtitle_en_calendarblock_subtitle_ua_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogpage',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
