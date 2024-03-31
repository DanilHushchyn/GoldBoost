# Generated by Django 5.0.2 on 2024-03-28 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_alter_catalogpage_calendar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_img', models.ImageField(upload_to='')),
                ('team_img_alt', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'teams',
            },
        ),
        migrations.RemoveField(
            model_name='calendarblockitem',
            name='team1_img',
        ),
        migrations.RemoveField(
            model_name='calendarblockitem',
            name='team1_img_alt',
        ),
        migrations.RemoveField(
            model_name='calendarblockitem',
            name='team1_img_alt_en',
        ),
        migrations.RemoveField(
            model_name='calendarblockitem',
            name='team1_img_alt_ua',
        ),
        migrations.RemoveField(
            model_name='calendarblockitem',
            name='team2_img',
        ),
        migrations.RemoveField(
            model_name='calendarblockitem',
            name='team2_img_alt',
        ),
        migrations.RemoveField(
            model_name='calendarblockitem',
            name='team2_img_alt_en',
        ),
        migrations.RemoveField(
            model_name='calendarblockitem',
            name='team2_img_alt_ua',
        ),
    ]
