# Generated by Django 5.0.2 on 2024-04-19 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_delete_orderfreqbotitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='freqbot',
        ),
    ]
