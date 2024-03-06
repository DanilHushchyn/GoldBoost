# Generated by Django 5.0.2 on 2024-03-06 11:35

import django.db.models.deletion
import src.products.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Tags',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('image_alt', models.CharField(max_length=255, null=True)),
                ('card_img', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('card_img_alt', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('price_type', models.CharField(choices=[('fixed', 'Fixed'), ('range', 'Range')], max_length=10)),
                ('bonus_points', models.IntegerField(default=0)),
                ('sale_percent', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sale_from', models.DateTimeField(blank=True, null=True)),
                ('sale_until', models.DateTimeField(blank=True, null=True)),
                ('bought_count', models.IntegerField(default=0)),
                ('catalog_page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='games.catalogpage')),
                ('tab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.tab')),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.tag')),
            ],
            options={
                'verbose_name': 'Products',
                'verbose_name_plural': 'Products',
                'ordering': ['-bought_count'],
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('Select', 'Select'), ('Radio', 'Radio'), ('CheckBox', 'CheckBox'), ('Slider', 'Slider')], max_length=50)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='products.product')),
            ],
            options={
                'verbose_name': 'Filters',
                'verbose_name_plural': 'Filters',
            },
        ),
        migrations.CreateModel(
            name='SubFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('filter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfilters', to='products.filter')),
            ],
        ),
    ]
