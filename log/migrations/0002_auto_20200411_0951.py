# Generated by Django 3.0.3 on 2020-04-11 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cachelog',
            name='cache_key',
            field=models.CharField(db_index=True, max_length=250, verbose_name='缓存key'),
        ),
    ]
