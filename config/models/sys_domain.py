from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from common.models import BaseModel


#模型主题域
class SysDomain(MPTTModel, BaseModel):
    domain_id = models.AutoField(primary_key=True, verbose_name='主题域标识')
    domain_name = models.CharField(max_length=250, verbose_name='主题域名称',db_index=True)
    domain_nbr = models.CharField(max_length=30, verbose_name='主题域编码', null=True, blank=True)
    par_domain = TreeForeignKey('self', on_delete=models.CASCADE, verbose_name='父级主题域标识',
                                blank=True, null=True, related_name='children')
    domain_desc = models.CharField(max_length=250, verbose_name='主题域描述', null=True, blank=True)

    def __str__(self):
        return u'%s' % self.domain_name

    class Meta:
        db_table = 'sys_domain'
        verbose_name_plural = "主题域"
        verbose_name = "主题域"


    class MPTTMeta:
        parent_attr = 'par_domain'
