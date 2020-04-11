from django.db import models
from django.db.models import ForeignKey

from common.models import BaseModel
from config.models.attr_spec import AttrSpec


# 属性值
class AttrValue(BaseModel):
    attr_value_id = models.AutoField(primary_key=True, verbose_name='属性值标识')
    attr_value = models.CharField(max_length=30, verbose_name='属性值', db_index=True)
    attr_value_name = models.CharField(max_length=30, verbose_name='属性值名称',db_index=True)
    attr = ForeignKey(AttrSpec, on_delete=models.CASCADE, verbose_name='属性')
    value_index = models.PositiveIntegerField(verbose_name='排序', default=1)

    def __str__(self):
        return u'%s' % self.attr_value_name

    class Meta:
        db_table = 'attr_value'
        verbose_name_plural = "属性值"
        verbose_name = "属性值"
        ordering = ['value_index']
