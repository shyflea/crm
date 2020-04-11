import datetime

from django.db import models

# Create your models here.
from common.attrs import get_attr_values, get_attr_default_value
from common.constants import GRANT_OBJ_TYPE_SYSTEM_USER, GRANT_OPER_TYPE_ALLOW, STATUS_ACTIVE, \
    GRANT_OBJ_TYPE_SYSTEM_POST, GRANT_OBJ_TYPE_SYSTEM_ROLES
from common.models import BaseModel
from ops.models.system_post import SystemPost
from ops.models.system_roles import SystemRoles
from ops.models.system_user import SystemUser


class Privilege(BaseModel):
    priv_id = models.AutoField(primary_key=True, verbose_name='权限标识')
    priv_code = models.CharField(max_length=30, verbose_name='权限编码', blank=True)
    priv_name = models.CharField(max_length=250, verbose_name='权限名称')
    priv_type = models.CharField(max_length=6, verbose_name='权限类型', choices=get_attr_values('Privilege', 'PRIV_TYPE'),
                                 default=get_attr_default_value('Privilege', 'PRIV_TYPE'))
    priv_desc = models.CharField(max_length=250, verbose_name='权限描述', blank=True, null=True)

    def __str__(self):
        return u'%s' % self.priv_name

    class Meta:
        db_table = 'privilege'
        verbose_name_plural = "权限"
        verbose_name = "权限"

    # 保存
    def save(self):
        if not self.priv_code:  # 如果未设置，则将权限编码默认为当前时间戳
            self.priv_code = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        super(Privilege, self).save()


class PrivFuncRel(BaseModel):
    priv_func_rel_id = models.AutoField(primary_key=True, verbose_name='权限包含功能标识')
    priv = models.ForeignKey(Privilege, on_delete=models.CASCADE, verbose_name='权限标识')
    priv_ref_type = models.CharField(max_length=250, verbose_name='关联功能类型')
    priv_ref_id = models.IntegerField(verbose_name='关联功能标识')

    class Meta:
        db_table = 'priv_func_rel'
        verbose_name_plural = "权限包含功能"
        verbose_name = "权限包含功能"


class PrivDataRel(BaseModel):
    priv_data_rel_id = models.AutoField(primary_key=True, verbose_name='权限包含数据标识')
    priv = models.ForeignKey(Privilege, on_delete=models.CASCADE, verbose_name='权限标识')
    priv_ref_id = models.IntegerField(verbose_name='关联业务对象标识')

    class Meta:
        db_table = 'priv_data_rel'
        verbose_name_plural = "权限包含数据"
        verbose_name = "权限包含数据"


class PrivGrant(BaseModel):
    priv_grant_id = models.AutoField(primary_key=True, verbose_name='授权标识')
    priv = models.ForeignKey(Privilege, on_delete=models.CASCADE, verbose_name='权限标识')
    grant_obj_type = models.CharField(max_length=10, verbose_name='授权对象类型',
                                      choices=get_attr_values('PrivGrant', 'GRANT_OBJ_TYPE'))
    grant_obj_id = models.IntegerField(verbose_name='授权对象标识')
    oper_type = models.CharField(max_length=4, verbose_name='授权操作类型',
                                 choices=get_attr_values('PrivGrant', 'GRANT_OPER_TYPE'))

    class Meta:
        db_table = 'priv_grant'
        verbose_name_plural = "授权"
        verbose_name = "授权"

    # 获取授权对象
    def grant_obj(self):
        obj = None
        if self.grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_USER:  # 系统用户
            obj = SystemUser.objects.get(sys_user_id=self.grant_obj_id)
        elif self.grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_POST:  # 系统岗位
            obj = SystemPost.objects.get(sys_user_id=self.grant_obj_id)
        elif self.grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_ROLES:  # 系统角色
            obj = SystemRoles.objects.get(sys_user_id=self.grant_obj_id)

        return obj

    grant_obj.short_description = u'授权对象'

    # 添加授权
    @staticmethod
    def add_priv_grant(priv_id, grant_obj_id, grant_obj_type):
        priv_grant = PrivGrant()
        priv_grant.priv_id = priv_id
        priv_grant.grant_obj_id = grant_obj_id
        priv_grant.grant_obj_type = grant_obj_type
        priv_grant.oper_type = GRANT_OPER_TYPE_ALLOW
        priv_grant.save()

    # 获取系统用户配置的权限(全部）
    @staticmethod
    def get_priv_grants(grant_obj_id, grant_obj_type):
        priv_grants = PrivGrant.objects.filter(grant_obj_id=grant_obj_id, status_cd=STATUS_ACTIVE,
                                               grant_obj_type=grant_obj_type)
        return priv_grants
