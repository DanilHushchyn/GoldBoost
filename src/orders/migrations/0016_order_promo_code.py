# Generated by Django 5.0.2 on 2024-03-30 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_orderitemattribute_title_en_and_more'),
        ('orders', '0015_remove_order_first_sale_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.promocode'),
        ),
    ]
