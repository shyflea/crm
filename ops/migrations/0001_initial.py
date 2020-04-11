# Generated by Django 3.0.3 on 2020-03-31 02:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import ops.manager.StaffManager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('sys_user_id', models.AutoField(primary_key=True, serialize=False, verbose_name='系统用户标识')),
                ('sys_user_code', models.CharField(max_length=250, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=250, verbose_name='密码')),
                ('pwd_err_cnt', models.IntegerField(default=3, null=True, verbose_name='密码错误次数限制')),
                ('pwd_sms_tel', models.IntegerField(blank=True, null=True, verbose_name='验证码短信通知手机号')),
                ('pwd_status', models.CharField(max_length=6, null=True, verbose_name='密码状态')),
                ('pwd_newtime', models.DateTimeField(auto_now_add=True)),
                ('pwd_effect_days', models.IntegerField(default=180, null=True, verbose_name='密码有效天数')),
                ('limit_count', models.IntegerField(default=180, null=True, verbose_name='登录次数限制')),
                ('logined_num', models.IntegerField(default=180, null=True, verbose_name='当前登录次数')),
                ('eff_date', models.DateTimeField(auto_now=True, null=True)),
                ('exp_date', models.DateTimeField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': '系统用户',
                'verbose_name_plural': '系统用户',
                'db_table': 'system_user',
            },
            managers=[
                ('objects', ops.manager.StaffManager.StaffManager()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('org_id', models.AutoField(primary_key=True, serialize=False, verbose_name='组织标识')),
                ('org_name', models.CharField(max_length=250, verbose_name='组织名称')),
                ('org_type', models.CharField(choices=[('1000', '内部组织'), ('1100', '外部组织')], default='1000', max_length=4, verbose_name='组织类型')),
                ('org_level', models.PositiveIntegerField(default=1, verbose_name='组织级别')),
                ('org_index', models.PositiveIntegerField(default=1, verbose_name='组织排序')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent_org', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ops.Organization', verbose_name='上级组织标识')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='config.CommonRegion', verbose_name='所在地区')),
            ],
            options={
                'verbose_name': '组织',
                'verbose_name_plural': '组织',
                'db_table': 'organization',
            },
        ),
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('priv_id', models.AutoField(primary_key=True, serialize=False, verbose_name='权限标识')),
                ('priv_code', models.CharField(blank=True, max_length=30, verbose_name='权限编码')),
                ('priv_name', models.CharField(max_length=250, verbose_name='权限名称')),
                ('priv_type', models.CharField(choices=[('1000', '功能权限'), ('1100', '数据权限'), ('1200', '混合权限')], default='1000', max_length=6, verbose_name='权限类型')),
                ('priv_desc', models.CharField(blank=True, max_length=250, null=True, verbose_name='权限描述')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
                'db_table': 'privilege',
            },
        ),
        migrations.CreateModel(
            name='SystemPost',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('sys_post_id', models.AutoField(primary_key=True, serialize=False, verbose_name='系统岗位标识')),
                ('sys_post_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='系统岗位编码')),
                ('sys_post_name', models.CharField(max_length=30, verbose_name='系统岗位名称')),
                ('sys_post_desc', models.CharField(blank=True, max_length=250, null=True, verbose_name='系统岗位描述')),
                ('init_flag', models.IntegerField(blank=True, choices=[(1, '是'), (0, '不是')], default=0, null=True, verbose_name='是否系统初始数据')),
            ],
            options={
                'verbose_name': '系统岗位',
                'verbose_name_plural': '系统岗位',
                'db_table': 'system_post',
            },
        ),
        migrations.CreateModel(
            name='SystemRoles',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('sys_role_id', models.AutoField(primary_key=True, serialize=False, verbose_name='系统角色标识')),
                ('sys_role_name', models.CharField(max_length=50, verbose_name='系统角色名称')),
                ('sys_role_code', models.CharField(blank=True, max_length=30, null=True, verbose_name='系统角色编码')),
                ('sys_role_desc', models.CharField(blank=True, max_length=250, null=True, verbose_name='系统角色描述')),
                ('init_flag', models.IntegerField(blank=True, choices=[(1, '是'), (0, '不是')], default=0, null=True, verbose_name='是否系统初始数据')),
            ],
            options={
                'verbose_name': '系统角色',
                'verbose_name_plural': '系统角色',
                'db_table': 'system_roles',
            },
        ),
        migrations.CreateModel(
            name='SystemUserRole',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('sys_user_role_id', models.AutoField(primary_key=True, serialize=False, verbose_name='系统角色标识')),
                ('sys_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.SystemRoles', verbose_name='系统角色标识')),
                ('sys_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='系统用户标识')),
            ],
            options={
                'verbose_name': '系统用户角色',
                'verbose_name_plural': '系统用户角色',
                'db_table': 'system_user_role',
            },
        ),
        migrations.CreateModel(
            name='SystemUserPost',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('sys_user_post_id', models.AutoField(primary_key=True, serialize=False, verbose_name='系统角色标识')),
                ('host_flag', models.IntegerField(blank=True, choices=[(1, '是'), (0, '不是')], default=1, null=True, verbose_name='是否主岗位')),
                ('org', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.Organization', verbose_name='隶属组织')),
                ('sys_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.SystemPost', verbose_name='系统岗位标识')),
                ('sys_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='系统用户标识')),
            ],
            options={
                'verbose_name': '系统用户任职岗位',
                'verbose_name_plural': '系统用户任职岗位',
                'db_table': 'system_user_post',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('staff_id', models.AutoField(primary_key=True, serialize=False, verbose_name='员工标识')),
                ('staff_code', models.CharField(max_length=250, null=True, verbose_name='员工编号')),
                ('staff_type', models.CharField(choices=[('1000', '内部员工'), ('1100', '外部员工')], default='1000', max_length=10, verbose_name='员工类型')),
                ('staff_name', models.CharField(max_length=250, verbose_name='员工姓名')),
                ('org', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.Organization', verbose_name='隶属组织')),
                ('region', mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='config.CommonRegion', verbose_name='所在地区')),
            ],
            options={
                'verbose_name': '员工',
                'verbose_name_plural': '员工',
                'db_table': 'staff',
            },
        ),
        migrations.CreateModel(
            name='PrivGrant',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('priv_grant_id', models.AutoField(primary_key=True, serialize=False, verbose_name='授权标识')),
                ('grant_obj_type', models.CharField(choices=[('1100', '系统用户'), ('1200', '系统岗位'), ('1300', '系统角色')], max_length=10, verbose_name='授权对象类型')),
                ('grant_obj_id', models.IntegerField(verbose_name='授权对象标识')),
                ('oper_type', models.CharField(choices=[('1000', '允许'), ('1100', '不允许')], max_length=4, verbose_name='授权操作类型')),
                ('priv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.Privilege', verbose_name='权限标识')),
            ],
            options={
                'verbose_name': '授权',
                'verbose_name_plural': '授权',
                'db_table': 'priv_grant',
            },
        ),
        migrations.CreateModel(
            name='PrivFuncRel',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('priv_func_rel_id', models.AutoField(primary_key=True, serialize=False, verbose_name='权限包含功能标识')),
                ('priv_ref_type', models.CharField(max_length=250, verbose_name='关联功能类型')),
                ('priv_ref_id', models.IntegerField(verbose_name='关联功能标识')),
                ('priv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.Privilege', verbose_name='权限标识')),
            ],
            options={
                'verbose_name': '权限包含功能',
                'verbose_name_plural': '权限包含功能',
                'db_table': 'priv_func_rel',
            },
        ),
        migrations.CreateModel(
            name='PrivDataRel',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('priv_data_rel_id', models.AutoField(primary_key=True, serialize=False, verbose_name='权限包含数据标识')),
                ('priv_ref_id', models.IntegerField(verbose_name='关联业务对象标识')),
                ('priv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.Privilege', verbose_name='权限标识')),
            ],
            options={
                'verbose_name': '权限包含数据',
                'verbose_name_plural': '权限包含数据',
                'db_table': 'priv_data_rel',
            },
        ),
        migrations.CreateModel(
            name='OrgPostRel',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('org_post_rel_id', models.AutoField(primary_key=True, serialize=False, verbose_name='组织标识')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.Organization', verbose_name='系统岗位标识')),
                ('sys_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.SystemPost', verbose_name='系统岗位标识')),
            ],
            options={
                'verbose_name': '组织使用系统岗位',
                'verbose_name_plural': '组织使用系统岗位',
                'db_table': 'org_post_rel',
            },
        ),
        migrations.CreateModel(
            name='FuncMenu',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_cd', models.CharField(default='1000', max_length=4, verbose_name='状态')),
                ('menu_id', models.AutoField(primary_key=True, serialize=False, verbose_name='菜单标识')),
                ('menu_name', models.CharField(db_index=True, max_length=50, verbose_name='菜单名称')),
                ('menu_type', models.CharField(choices=[('1000', '目录菜单'), ('1100', '叶子菜单')], max_length=4, verbose_name='菜单类型')),
                ('menu_level', models.PositiveIntegerField(default=1, verbose_name='菜单级别')),
                ('menu_index', models.PositiveIntegerField(default=1, verbose_name='菜单排序')),
                ('url_addr', models.CharField(blank=True, max_length=250, verbose_name='菜单地址')),
                ('menu_desc', models.CharField(blank=True, max_length=250, verbose_name='菜单描述')),
                ('icon', models.CharField(db_index=True, default='far fa-surprise', max_length=50, verbose_name='菜单图标')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('par_menu', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ops.FuncMenu', verbose_name='上级菜单')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
                'db_table': 'func_menu',
                'ordering': ('menu_index',),
            },
        ),
        migrations.AddField(
            model_name='systemuser',
            name='staff',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ops.Staff', verbose_name='员工'),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]