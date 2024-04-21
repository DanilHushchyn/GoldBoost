# Generated by Django 5.0.2 on 2024-04-21 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_remove_order_promo_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='cartitem',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
