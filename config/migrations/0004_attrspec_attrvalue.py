# Generated by Django 3.0.3 on 2020-03-31 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_sysclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttrSpec',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('attr_id', models.AutoField(primary_key=True, serialize=False, verbose_name='属性标识')),
                ('attr_nbr', models.CharField(db_index=True, max_length=30, verbose_name='属性编码')),
                ('attr_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='属性名称')),
                ('default_value', models.CharField(max_length=250, null=True, verbose_name='默认值')),
                ('sys_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.SysClass', verbose_name='主题域')),
            ],
            options={
                'verbose_name': '属性',
                'verbose_name_plural': '属性',
                'db_table': 'attr_spec',
            },
        ),
        migrations.CreateModel(
            name='AttrValue',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('attr_value_id', models.AutoField(primary_key=True, serialize=False, verbose_name='属性值标识')),
                ('attr_value', models.CharField(db_index=True, max_length=30, verbose_name='属性值')),
                ('attr_value_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='属性值名称')),
                ('value_index', models.PositiveIntegerField(default=1, verbose_name='排序')),
                ('attr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.AttrSpec', verbose_name='属性标识')),
            ],
            options={
                'verbose_name': '属性值',
                'verbose_name_plural': '属性值',
                'db_table': 'attr_value',
            },
        ),
    ]
