# Generated by Django 5.0.2 on 2024-04-11 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_subfilter_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subfilter',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
