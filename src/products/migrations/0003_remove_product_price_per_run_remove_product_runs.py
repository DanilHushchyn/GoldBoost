# Generated by Django 5.0.2 on 2024-03-05 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_filter_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_per_run',
        ),
        migrations.RemoveField(
            model_name='product',
            name='runs',
        ),
    ]
