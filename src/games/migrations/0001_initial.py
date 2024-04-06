# Generated by Django 5.0.2 on 2024-04-04 18:57

import django.db.models.deletion
import meta.models
import src.products.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Calendar',
                'verbose_name_plural': 'Calendars',
                'db_table': 'calendars',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('logo_filter', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('logo_product', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('logo_filter_alt', models.CharField(max_length=255, null=True)),
                ('logo_filter_alt_en', models.CharField(max_length=255, null=True)),
                ('logo_filter_alt_uk', models.CharField(max_length=255, null=True)),
                ('logo_product_alt', models.CharField(max_length=255, null=True)),
                ('logo_product_alt_en', models.CharField(max_length=255, null=True)),
                ('logo_product_alt_uk', models.CharField(max_length=255, null=True)),
                ('order', models.IntegerField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Games',
                'verbose_name_plural': 'Games',
                'db_table': 'games',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_img', models.ImageField(upload_to='')),
                ('team_img_alt', models.CharField(max_length=255, null=True)),
                ('team_img_alt_en', models.CharField(max_length=255, null=True)),
                ('team_img_alt_uk', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'teams',
            },
        ),
        migrations.CreateModel(
            name='WorthLook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Worth look',
                'verbose_name_plural': 'Worth look',
                'db_table': 'worth_look',
            },
        ),
        migrations.CreateModel(
            name='CalendarBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('title_uk', models.CharField(max_length=255, null=True)),
                ('subtitle', models.CharField(max_length=255)),
                ('subtitle_en', models.CharField(max_length=255, null=True)),
                ('subtitle_uk', models.CharField(max_length=255, null=True)),
                ('calendar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='games.calendar')),
            ],
            options={
                'verbose_name': 'Calendar Block',
                'verbose_name_plural': 'Calendar Blocks',
                'db_table': 'calendar_blocks',
            },
        ),
        migrations.CreateModel(
            name='CatalogPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('title_en', models.CharField(null=True)),
                ('title_uk', models.CharField(null=True)),
                ('description', models.TextField()),
                ('description_en', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('order', models.IntegerField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('calendar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.calendar')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='games.catalogpage')),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_pages', related_query_name='game', to='games.game')),
                ('worth_look', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.worthlook')),
            ],
            options={
                'verbose_name': 'Catalog Page',
                'verbose_name_plural': 'Catalog Pages',
                'db_table': 'catalog_pages',
                'ordering': ['order'],
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.CreateModel(
            name='CatalogTabs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('title_en', models.CharField(null=True)),
                ('title_uk', models.CharField(null=True)),
                ('content', models.TextField()),
                ('content_en', models.TextField(null=True)),
                ('content_uk', models.TextField(null=True)),
                ('order', models.PositiveIntegerField(null=True)),
                ('catalog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tabs', to='games.catalogpage')),
            ],
            options={
                'verbose_name': 'Catalog Tab',
                'verbose_name_plural': 'Catalog Tabs',
                'db_table': 'catalog_tabs',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='CalendarBlockItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('team1_from', models.TimeField()),
                ('team1_until', models.TimeField()),
                ('team2_from', models.TimeField()),
                ('team2_until', models.TimeField()),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='games.calendarblock')),
                ('team1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calendars1', related_query_name='team1', to='games.team')),
                ('team2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calendars2', related_query_name='team2', to='games.team')),
            ],
            options={
                'db_table': 'calendar_block_items',
            },
        ),
        migrations.CreateModel(
            name='WorthLookItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('image_alt', models.CharField(max_length=255, null=True)),
                ('image_alt_en', models.CharField(max_length=255, null=True)),
                ('image_alt_uk', models.CharField(max_length=255, null=True)),
                ('carousel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='games.worthlook')),
                ('catalog_page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='games.catalogpage')),
            ],
            options={
                'verbose_name': 'Worth look item',
                'verbose_name_plural': 'Worth look items',
                'db_table': 'worth_look_items',
            },
        ),
    ]
