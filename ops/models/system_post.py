from django.db import models

from common.attrs import get_attr_values
from common.constants import FALSE
from common.models import BaseModel


class SystemPost(BaseModel):
    sys_post_id = models.AutoField(primary_key=True, verbose_name='系统岗位标识')
    sys_post_code = models.CharField(max_length=50, verbose_name='系统岗位编码', null=True, blank=True)
    sys_post_name = models.CharField(max_length=30, verbose_name='系统岗位名称')
    sys_post_desc = models.CharField(max_length=250, verbose_name='系统岗位描述', null=True, blank=True)
    init_flag = models.IntegerField(verbose_name='是否系统初始数据', choices=get_attr_values('BaseModel', 'TRUE_OR_FALSE'),
                                    null=True, blank=True, default=FALSE)

    class Meta:
        db_table = 'system_post'
        verbose_name_plural = "系统岗位"
        verbose_name = "系统岗位"

    def __str__(self):
        return u'%s' % self.sys_post_name
