# Generated by Django 5.0.2 on 2024-04-25 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='battle_tag',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]