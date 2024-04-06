# Generated by Django 5.0.2 on 2024-04-04 18:57

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=500, null=True)),
            ],
            options={
                'db_table': 'carts',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'cart_items',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('number', models.PositiveBigIntegerField(null=True, unique=True)),
                ('status', models.CharField(choices=[('IN PROGRESS', 'IN PROGRESS'), ('CANCELED', 'CANCELED'), ('COMPLETED', 'COMPLETED')], default='CANCELED', max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.FloatField()),
            ],
            options={
                'verbose_name': 'Orders',
                'verbose_name_plural': 'Orders',
                'db_table': 'orders',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_filter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.subfilter')),
            ],
            options={
                'db_table': 'attributes',
            },
        ),
    ]
