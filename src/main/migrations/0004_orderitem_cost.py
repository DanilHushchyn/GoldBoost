# Generated by Django 5.0.2 on 2024-04-15 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='cost',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
