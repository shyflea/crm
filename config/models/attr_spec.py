from django.db import models
from django.db.models import ForeignKey

from common.models import BaseModel


# 属性表
from config.models.sys_class import SysClass


class AttrSpec(BaseModel):
    attr_id = models.AutoField(primary_key=True, verbose_name='属性标识')
    attr_nbr = models.CharField(max_length=30, verbose_name='属性编码', db_index=True)
    attr_name = models.CharField(max_length=30, verbose_name='属性名称')
    default_value = models.CharField(max_length=250, verbose_name='默认值', null=True,blank=True)
    sys_class = ForeignKey(SysClass, on_delete=models.CASCADE, verbose_name='类')

    def __str__(self):
        return u'%s' % self.attr_name

    class Meta:

        db_table = 'attr_spec'
        verbose_name_plural = "属性"
        verbose_name = "属性"
