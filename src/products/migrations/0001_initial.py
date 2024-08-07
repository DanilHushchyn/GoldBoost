# Generated by Django 5.0.2 on 2024-04-21 22:10

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
                ('name_en', models.CharField(max_length=255, null=True)),
                ('name_uk', models.CharField(max_length=255, null=True)),
                ('color', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Tags',
                'verbose_name_plural': 'Tags',
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('title_uk', models.CharField(max_length=255, null=True)),
                ('subtitle', models.CharField(max_length=255)),
                ('subtitle_en', models.CharField(max_length=255, null=True)),
                ('subtitle_uk', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('image_alt', models.CharField(max_length=255, null=True)),
                ('image_alt_en', models.CharField(max_length=255, null=True)),
                ('image_alt_uk', models.CharField(max_length=255, null=True)),
                ('card_img', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('card_img_alt', models.CharField(max_length=255, null=True)),
                ('card_img_alt_en', models.CharField(max_length=255, null=True)),
                ('card_img_alt_uk', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('description_en', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('price', models.FloatField()),
                ('price_type', models.CharField(choices=[('fixed', 'Fixed'), ('range', 'Range')], max_length=10)),
                ('bonus_points', models.IntegerField(default=0)),
                ('sale_percent', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sale_from', models.DateTimeField(blank=True, null=True)),
                ('sale_until', models.DateTimeField(blank=True, null=True)),
                ('bought_count', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('catalog_page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='games.catalogpage')),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.tag')),
            ],
            options={
                'verbose_name': 'Products',
                'verbose_name_plural': 'Products',
                'db_table': 'products',
                'ordering': ['-bought_count'],
            },
        ),
        migrations.CreateModel(
            name='FreqBought',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(null=True)),
                ('order', models.PositiveSmallIntegerField(null=True)),
                ('discount', models.PositiveSmallIntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('products', models.ManyToManyField(blank=True, to='products.product')),
            ],
            options={
                'verbose_name': 'Frequently Bought',
                'verbose_name_plural': 'Frequently Bought',
                'db_table': 'freq_bought',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('title_uk', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(choices=[('Select', 'Select'), ('Radio', 'Radio'), ('CheckBox', 'CheckBox'), ('Slider', 'Slider')], max_length=50)),
                ('order', models.PositiveIntegerField(null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='products.product')),
            ],
            options={
                'verbose_name': 'Filters',
                'verbose_name_plural': 'Filters',
                'db_table': 'filters',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ProductTabs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('title_en', models.CharField(null=True)),
                ('title_uk', models.CharField(null=True)),
                ('content', models.TextField()),
                ('content_en', models.TextField(null=True)),
                ('content_uk', models.TextField(null=True)),
                ('order', models.PositiveIntegerField(null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tabs', to='products.product')),
            ],
            options={
                'verbose_name': 'Product Tab',
                'verbose_name_plural': 'Product Tabs',
                'db_table': 'product_tabs',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='SubFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('title_uk', models.CharField(max_length=255, null=True)),
                ('price', models.FloatField()),
                ('order', models.PositiveIntegerField(null=True)),
                ('filter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfilters', to='products.filter')),
            ],
            options={
                'verbose_name': 'SubFilter',
                'verbose_name_plural': 'SubFilters',
                'db_table': 'sub_filters',
                'ordering': ['order'],
            },
        ),
    ]
