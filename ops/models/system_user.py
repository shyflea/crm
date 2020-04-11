from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from mptt.fields import TreeForeignKey

from common.attrs import get_attr_values
from common.constants import STATUS_ACTIVE, GRANT_OBJ_TYPE_SYSTEM_USER, GRANT_OPER_TYPE_ALLOW, TRUE, \
    GRANT_OBJ_TYPE_SYSTEM_POST, GRANT_OBJ_TYPE_SYSTEM_ROLES
from common.models import BaseModel
from common.utils import make_md5
from ops.manager.StaffManager import StaffManager
from ops.models.organization import Organization
from ops.models.staff import Staff
from ops.models.system_post import SystemPost
from ops.models.system_roles import SystemRoles


class SystemUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    sys_user_id = models.AutoField(primary_key=True, verbose_name='系统用户标识')
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, verbose_name='员工')
    sys_user_code = models.CharField(max_length=250, verbose_name='账号', unique=True)
    password = models.CharField(max_length=250, verbose_name='密码')
    pwd_err_cnt = models.IntegerField(verbose_name='密码错误次数限制', default=3, null=True)
    pwd_sms_tel = models.IntegerField(verbose_name='验证码短信通知手机号', null=True, blank=True)
    pwd_status = models.CharField(max_length=6, verbose_name='密码状态', null=True)
    pwd_newtime = models.DateTimeField(auto_now_add=True)  # 新密码生成时间
    pwd_effect_days = models.IntegerField(verbose_name='密码有效天数', default=180, null=True)
    limit_count = models.IntegerField(verbose_name='登录次数限制', default=180, null=True)
    logined_num = models.IntegerField(verbose_name='当前登录次数', default=180, null=True)
    eff_date = models.DateTimeField(auto_now=True, null=True)  # 新密码生成时间
    exp_date = models.DateTimeField(null=True)  # 新密码生成时间

    # 指定用于验证的系统账号
    USERNAME_FIELD = 'sys_user_code'
    # 除用户名、密码，需要提醒用户输入的字段
    REQUIRED_FIELDS = []
    # 重新定义Manager对象，创建用户时使用
    objects = StaffManager()

    class Meta:
        db_table = 'system_user'
        verbose_name_plural = "系统用户"
        verbose_name = "系统用户"

    def __str__(self):
        return ''

    # django 必须重写的属性
    @property
    def is_active(self):
        if self.status_cd == STATUS_ACTIVE:
            return True
        return False

    # django 必须重写的属性
    @property
    def is_staff(self):
        return True

    # 密码验证(重写django的方法）
    def check_password(self, password):
        if self.password == make_md5(password):
            return True
        return False

    # 密码加密(重写django的方法，密码修改的时候会调用到）
    def set_password(self, raw_password):
        self.password = make_md5(raw_password)
        self._password = raw_password

    # django 必须重写的方法
    def get_full_name(self):
        return self.sys_user_code

    # django 必须重写的方法
    def get_short_name(self):
        return self.sys_user_code

    # 重写django的鉴权方法
    def has_perm(self, priv_code):
        # 超级用户拥有所有权限
        if self.is_active and self.is_superuser:
            return True

        if not priv_code:
            return False
        # 根据权限编码查权限
        from ops.models.privilege import Privilege
        priv = Privilege.objects.filter(priv_code=priv_code).first()
        # django自动生成的权限，如果我们自己的权限配置未配置，则默认有权限
        if priv is None:
            return True
        # 判断用户是否有权限
        if self.has_perm_by_priv_id(priv.priv_id):
            return True
        return False

    """ 
    根据权限ID判断用户是否具有该权限
    """
    def has_perm_by_priv_id(self, priv_id):
        # 超级用户拥有所有权限
        if self.is_active and self.is_superuser:
            return True

        # 授权规则
        # 授权规则1：系统用户
        priv_grants = self.get_priv_grants_by_user(priv_id)
        # 授权规则2：系统岗位
        priv_grants_post = self.get_priv_grants_by_post(priv_id)
        if priv_grants_post is not None and len(priv_grants_post) > 0:
            priv_grants = priv_grants | priv_grants_post
        # 授权规则3：系统角色
        priv_grants_role = self.get_priv_grants_by_role(priv_id)
        if priv_grants_role is not None and len(priv_grants_role) > 0:
            priv_grants = priv_grants | priv_grants_role
        # 判断是否有权限
        if len(priv_grants) > 0:
            for priv_grant in priv_grants:
                if priv_grant.oper_type == GRANT_OPER_TYPE_ALLOW:
                    return True
                else:
                    return False
        return False

    # 获取系统用户配置的权限（某一权限）
    def get_priv_grants_by_user(self, priv_id):
        from ops.models.privilege import PrivGrant
        priv_grants = PrivGrant.objects.filter(grant_obj_id=self.sys_user_id, status_cd=STATUS_ACTIVE,
                                               grant_obj_type=GRANT_OBJ_TYPE_SYSTEM_USER, priv_id=priv_id)
        return priv_grants

    # 获取系统用户配置的权限(全部）
    def get_priv_grants_by_user_all(self):
        from ops.models.privilege import PrivGrant
        priv_grants = PrivGrant.objects.filter(grant_obj_id=self.sys_user_id, status_cd=STATUS_ACTIVE,
                                               grant_obj_type=GRANT_OBJ_TYPE_SYSTEM_USER)
        return priv_grants

    # 获取岗位配置的权限
    def get_priv_grants_by_post(self, priv_id):
        from ops.models.privilege import PrivGrant
        priv_grants = None
        system_user_posts = SystemUserPost.objects.filter(sys_user_id=self.sys_user_id, status_cd=STATUS_ACTIVE)
        if len(system_user_posts) > 0:
            for system_user_post in system_user_posts:
                priv_grants_position = PrivGrant.objects.filter(grant_obj_id=system_user_post.sys_post.sys_post_id,
                                                                status_cd=STATUS_ACTIVE,
                                                                grant_obj_type=GRANT_OBJ_TYPE_SYSTEM_POST,
                                                                priv_id=priv_id)
                if priv_grants is None:
                    priv_grants = priv_grants_position
                else:
                    priv_grants = priv_grants | priv_grants_position
        return priv_grants

    # 获取角色配置的权限
    def get_priv_grants_by_role(self, priv_id):
        from ops.models.privilege import PrivGrant
        priv_grants = None
        system_user_roles = SystemUserRole.objects.filter(sys_user_id=self.sys_user_id, status_cd=STATUS_ACTIVE)
        if len(system_user_roles) > 0:
            for system_user_role in system_user_roles:
                priv_grants_role = PrivGrant.objects.filter(grant_obj_id=system_user_role.sys_role.sys_role_id,
                                                            status_cd=STATUS_ACTIVE,
                                                            grant_obj_type=GRANT_OBJ_TYPE_SYSTEM_ROLES,
                                                            priv_id=priv_id)
                if priv_grants is None:
                    priv_grants = priv_grants_role
                else:
                    priv_grants = priv_grants | priv_grants_role
        return priv_grants

    # 获取系统用户任职岗位
    def get_system_user_post(self, org_id):
        system_user_post = SystemUserPost.objects.filter(org_id=org_id, sys_user_id=self.sys_user_id,
                                                         status_cd=STATUS_ACTIVE).first()
        return system_user_post

    # 获取系统用户角色
    def get_system_user_roles(self):
        system_user_roles = SystemUserRole.objects.filter(sys_user_id=self.sys_user_id,
                                                          status_cd=STATUS_ACTIVE)
        return system_user_roles

    # 根据员工ID系统用户角色
    def get_system_user_roles_by_staff_id(staff_id):
        system_user_roles = None
        system_user = SystemUser.objects.filter(staff_id=staff_id, status_cd=STATUS_ACTIVE).first()
        if system_user:
            system_user_roles = SystemUserRole.objects.filter(sys_user_id=system_user.sys_user_id,
                                                              status_cd=STATUS_ACTIVE)
        return system_user_roles

    # 保存岗位和角色
    def save_post_and_role(self, org_id, post, roles):
        # 保存岗位

        system_user_post = self.get_system_user_post(org_id)
        insert = False
        if post:
            if system_user_post:
                if system_user_post.sys_post_id is not post:
                    system_user_post.delete()
                    insert = True
            else:
                insert = True
        if insert is True:
            system_user_post = SystemUserPost()
            system_user_post.sys_post_id = post
            system_user_post.org_id = org_id
            system_user_post.sys_user_id = self.sys_user_id
            system_user_post.save()
        # 保存角色
        role_list = []
        if roles:
            role_list = str(roles).split(',')
        system_user_roles = self.get_system_user_roles()
        # 本次去选了原有的角色, 则角色删除
        keep = []
        if len(system_user_roles) > 0:
            for system_user_role in system_user_roles:
                if len(roles) == 0 or system_user_role.sys_role.sys_role_name not in role_list:
                    system_user_role.delete()
                else:
                    keep.append(system_user_role.sys_role.sys_role_name)
        # 角色不存在则新增
        if len(role_list) > 0:
            for role_name in role_list:
                add = False
                if len(system_user_roles) == 0:
                    add = True
                elif role_name not in keep:
                    add = True
                if add is True:
                    system_user_role = SystemUserRole()
                    # 由于element-ui的多选框控件的lable、vulue共用label，导致vulue只能是角色名称，因此只能先用名称查询
                    system_roles = SystemRoles.objects.filter(sys_role_name=role_name, status_cd=STATUS_ACTIVE).first()

                    if system_roles:
                        system_user_role.sys_role_id = system_roles.sys_role_id
                        system_user_role.sys_user_id = self.sys_user_id
                        system_user_role.save()


class SystemUserRole(BaseModel):
    sys_user_role_id = models.AutoField(primary_key=True, verbose_name='系统角色标识')
    sys_role = models.ForeignKey(SystemRoles, on_delete=models.CASCADE, verbose_name='系统角色标识')
    sys_user = models.ForeignKey(SystemUser, on_delete=models.CASCADE, verbose_name='系统用户标识')

    class Meta:
        db_table = 'system_user_role'
        verbose_name_plural = "系统用户角色"
        verbose_name = "系统用户角色"


class SystemUserPost(BaseModel):
    sys_user_post_id = models.AutoField(primary_key=True, verbose_name='系统角色标识')
    sys_post = models.ForeignKey(SystemPost, on_delete=models.CASCADE, verbose_name='系统岗位标识')
    sys_user = models.ForeignKey(SystemUser, on_delete=models.CASCADE, verbose_name='系统用户标识')
    org = TreeForeignKey(Organization, on_delete=models.CASCADE, verbose_name='隶属组织')
    host_flag = models.IntegerField(verbose_name='是否主岗位', choices=get_attr_values('BaseModel', 'TRUE_OR_FALSE'),
                                    null=True, blank=True, default=TRUE)

    class Meta:
        db_table = 'system_user_post'
        verbose_name_plural = "系统用户任职岗位"
        verbose_name = "系统用户任职岗位"
