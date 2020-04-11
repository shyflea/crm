from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
from common.attrs import get_attr_values, get_attr_default_value
from common.models import BaseModel
from config.models.common_region import CommonRegion
from ops.models.system_post import SystemPost


class Organization(MPTTModel, BaseModel):
    org_id = models.AutoField(primary_key=True, verbose_name='组织标识')
    org_name = models.CharField(max_length=250, verbose_name='组织名称')
    org_type = models.CharField(max_length=4, verbose_name='组织类型', choices= get_attr_values('Organization', 'ORG_TYPE'),
                                default=get_attr_default_value('Organization', 'ORG_TYPE'))
    org_level = models.PositiveIntegerField(verbose_name='组织级别', default=1)
    org_index = models.PositiveIntegerField(verbose_name='组织排序', default=1)
    parent_org = TreeForeignKey('self', on_delete=models.CASCADE, verbose_name='上级组织标识',
                                blank=True, null=True, related_name='children')
    region = models.ForeignKey(CommonRegion, on_delete=models.CASCADE, verbose_name='所在地区', null=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['org_type'].choices = get_attr_values('Organization', 'ORG_TYPE')
    #     self.fields['org_type'].default = get_attr_default_value('Organization', 'ORG_TYPE')

    def __str__(self):
        return u'%s' % self.org_name

    class Meta:
        db_table = 'organization'
        verbose_name_plural = "组织"
        verbose_name = "组织"

    class MPTTMeta:
        parent_attr = 'parent_org'
        level_attr = 'org_level'
        order_insertion_by = ['org_index']


class OrgPostRel(BaseModel):
    org_post_rel_id = models.AutoField(primary_key=True, verbose_name='组织标识')
    sys_post = models.ForeignKey(SystemPost, on_delete=models.CASCADE, verbose_name='系统岗位标识')
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='系统岗位标识')

    class Meta:
        db_table = 'org_post_rel'
        verbose_name_plural = "组织使用系统岗位"
        verbose_name = "组织使用系统岗位"
