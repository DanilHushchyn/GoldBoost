# -*- coding: utf-8 -*-
# Generated by Django 5.0.2 on 2024-04-05 13:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_remove_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=255, null=True),
        ),
    ]