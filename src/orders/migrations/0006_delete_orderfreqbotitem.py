# Generated by Django 5.0.2 on 2024-04-19 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderfreqbotitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderFreqBotItem',
        ),
    ]