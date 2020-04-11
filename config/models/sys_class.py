from django.db import models
from mptt.models import TreeForeignKey

from common.models import BaseModel
from config.models.sys_domain import SysDomain


# 系统类
class SysClass(BaseModel):
    class_id = models.AutoField(primary_key=True, verbose_name='系统类标识')
    class_name = models.CharField(max_length=30, verbose_name='类名', db_index=True)
    table_code = models.CharField(max_length=30, verbose_name='表英文名', null=True, blank=True, db_index=True)
    table_name = models.CharField(max_length=250, verbose_name='表中文名', null=True, blank=True,db_index=True)
    domain = TreeForeignKey(SysDomain, on_delete=models.CASCADE, verbose_name='主题域')

    def __str__(self):
        return u'%s' % self.table_name

    class Meta:
        db_table = 'sys_class'
        verbose_name_plural = "系统类"
        verbose_name = "系统类"
        ordering =['domain_id','class_id']
