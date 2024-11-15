# Generated by Django 5.0.2 on 2024-04-21 22:10

import django.core.validators
import django.db.models.deletion
import src.products.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('img_alt', models.CharField(max_length=255, null=True)),
                ('img_alt_en', models.CharField(max_length=255, null=True)),
                ('img_alt_uk', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Insta',
                'verbose_name_plural': 'Insta',
                'db_table': 'insta',
            },
        ),
        migrations.CreateModel(
            name='OrderItemAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('title_uk', models.CharField(max_length=255, null=True)),
                ('subtitle', models.CharField(max_length=255, null=True)),
                ('subtitle_en', models.CharField(max_length=255, null=True)),
                ('subtitle_uk', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'sub_orders_attributes',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=215)),
                ('from_date', models.DateField()),
                ('until_date', models.DateField()),
                ('discount', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Promo codes',
                'verbose_name_plural': 'Promo codes',
                'db_table': 'promo_codes',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255, null=True)),
                ('author_en', models.CharField(max_length=255, null=True)),
                ('author_uk', models.CharField(max_length=255, null=True)),
                ('comment', models.TextField()),
                ('comment_en', models.TextField(null=True)),
                ('comment_uk', models.TextField(null=True)),
                ('stars_count', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('source_of_review', models.CharField(max_length=255)),
                ('source_of_review_url', models.URLField(null=True)),
                ('date_published', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'db_table': 'reviews',
                'ordering': ['-date_published'],
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_nickname', models.CharField(max_length=255)),
                ('instagram_link', models.URLField()),
                ('facebook_link', models.URLField()),
                ('reddit_link', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('discord_link', models.URLField()),
                ('whats_up_link', models.URLField()),
                ('header_top_text', models.CharField(max_length=255)),
                ('header_top_text_en', models.CharField(max_length=255, null=True)),
                ('header_top_text_uk', models.CharField(max_length=255, null=True)),
                ('footer_bottom_text', models.CharField(max_length=255)),
                ('footer_description', models.TextField()),
                ('footer_description_en', models.TextField(null=True)),
                ('footer_description_uk', models.TextField(null=True)),
                ('privacy_policy_link', models.URLField()),
                ('terms_of_use_link', models.URLField()),
                ('refund_policy_link', models.URLField()),
                ('address1', models.CharField(max_length=255)),
                ('address1_en', models.CharField(max_length=255, null=True)),
                ('address1_uk', models.CharField(max_length=255, null=True)),
                ('address1_link', models.URLField(null=True)),
                ('address2', models.CharField(max_length=255)),
                ('address2_en', models.CharField(max_length=255, null=True)),
                ('address2_uk', models.CharField(max_length=255, null=True)),
                ('address2_link', models.URLField(null=True)),
                ('subscribe_form_text', models.CharField(max_length=255)),
                ('subscribe_form_text_en', models.CharField(max_length=255, null=True)),
                ('subscribe_form_text_uk', models.CharField(max_length=255, null=True)),
                ('subscribe_sale', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
                'db_table': 'settings',
            },
        ),
        migrations.CreateModel(
            name='WhyChooseUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('icon_alt', models.CharField(max_length=255, null=True)),
                ('icon_alt_en', models.CharField(max_length=255, null=True)),
                ('icon_alt_uk', models.CharField(max_length=255, null=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('title_uk', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('description_en', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'WhyChooseUs',
                'verbose_name_plural': 'WhyChooseUs',
                'db_table': 'why_choose_us',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('title_en', models.CharField(default='', max_length=255, null=True)),
                ('title_uk', models.CharField(default='', max_length=255, null=True)),
                ('image', models.ImageField(null=True, upload_to=src.products.utils.get_timestamp_path)),
                ('image_alt', models.CharField(max_length=255, null=True)),
                ('image_alt_en', models.CharField(max_length=255, null=True)),
                ('image_alt_uk', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('description_en', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('date_published', models.DateField(auto_now_add=True)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
                'db_table': 'news',
                'ordering': ['-date_published'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField(null=True)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('freqbot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.freqbought')),
            ],
            options={
                'db_table': 'sub_orders',
                'ordering': ['-date_created'],
            },
        ),
    ]
