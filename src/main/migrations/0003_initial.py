# Generated by Django 5.0.2 on 2024-04-21 22:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='users',
            field=models.ManyToManyField(related_name='promo_codes', to=settings.AUTH_USER_MODEL),
        ),
    ]
