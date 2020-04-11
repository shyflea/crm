from django.db import models

from common.attrs import get_attr_values
from common.constants import FALSE
from common.models import BaseModel


class SystemRoles(BaseModel):
    sys_role_id = models.AutoField(primary_key=True, verbose_name='系统角色标识')
    sys_role_name = models.CharField(max_length=50, verbose_name='系统角色名称')
    sys_role_code = models.CharField(max_length=30, verbose_name='系统角色编码', null=True, blank=True)
    sys_role_desc = models.CharField(max_length=250, verbose_name='系统角色描述', null=True, blank=True)
    init_flag = models.IntegerField(verbose_name='是否系统初始数据', choices=get_attr_values('BaseModel', 'TRUE_OR_FALSE'),
                                    null=True, blank=True, default=FALSE)

    class Meta:
        db_table = 'system_roles'
        verbose_name_plural = "系统角色"
        verbose_name = "系统角色"

    def __str__(self):
        return u'%s' % self.sys_role_name
