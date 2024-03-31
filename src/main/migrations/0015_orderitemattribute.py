# Generated by Django 5.0.2 on 2024-03-29 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_setting_subscribe_sale_active'),
        ('products', '0022_alter_freqbought_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItemAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('order_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='main.orderitem')),
                ('subfilter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.subfilter')),
            ],
            options={
                'db_table': 'sub_orders_attributes',
            },
        ),
    ]
