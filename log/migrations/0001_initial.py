# Generated by Django 3.0.3 on 2020-04-11 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CacheLog',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('log_id', models.AutoField(primary_key=True, serialize=False, verbose_name='日志标志')),
                ('cache_type', models.CharField(db_index=True, max_length=30, verbose_name='缓存类型')),
                ('cache_key', models.CharField(db_index=True, max_length=30, verbose_name='缓存key')),
                ('cache_value', models.TextField(blank=True, null=True, verbose_name='缓存值')),
                ('timeout', models.IntegerField(verbose_name='缓存失效时间')),
            ],
            options={
                'verbose_name': '缓存日志',
                'verbose_name_plural': '缓存日志',
                'db_table': 'cache_log',
            },
        ),
    ]
