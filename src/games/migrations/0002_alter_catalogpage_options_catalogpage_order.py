# Generated by Django 5.0.2 on 2024-03-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalogpage',
            options={'ordering': ['order'], 'verbose_name': 'Catalog Page', 'verbose_name_plural': 'Catalog Pages'},
        ),
        migrations.AddField(
            model_name='catalogpage',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
