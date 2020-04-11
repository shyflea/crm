import re

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from pypinyin import pinyin, Style

# Create your models here.
from common.attrs import get_attr_values
from common.constants import REGION_TYPE_COUNTRY, REGION_TYPE_PROVINCE, REGION_TYPE_CITY, REGION_TYPE_COUNTY
from common.models import BaseModel


class CommonRegion(MPTTModel, BaseModel):
    common_region_id = models.AutoField(primary_key=True, verbose_name='公共管理区域标识')
    region_name = models.CharField(max_length=250, verbose_name='区域名称', db_index=True)
    region_py_name = models.CharField(max_length=250, verbose_name='区域拼音名称', null=True, blank=True)
    region_nbr = models.CharField(max_length=30, verbose_name='区域编码', null=True, blank=True)
    region_type = models.CharField(max_length=6, verbose_name='区域类型',
                                   choices=get_attr_values('CommonRegion', 'REGION_TYPE'), null=True)
    par_region = TreeForeignKey('self', on_delete=models.CASCADE, verbose_name='上级区域标识',
                                blank=True, null=True, related_name='children')
    region_level = models.PositiveIntegerField(verbose_name='区域级别')
    province_nbr = models.CharField(max_length=32, verbose_name='省份编码', null=True, blank=True)
    remark = models.CharField(max_length=250, verbose_name='备注', null=True, blank=True)

    def __str__(self):
        return u'%s' % self.region_name

    # 获取完成区域名称，如 中国/福建省/厦门市/湖里区
    @property
    def whole_region_name(self):
        region_name = ''
        regions = []
        regions.append(self.region_name)
        par_region = self.par_region
        while par_region:
            regions.append(par_region.region_name)
            par_region = par_region.par_region

        if len(regions) > 0:
            region_name = "/".join(map(str, [region for region in reversed(regions)]))
        return region_name

    # 保存
    def save(self):
        # 自动设置区域拼音名称
        region_name = re.sub('省|市|区|县|自治|回族|', '', self.region_name)
        words = pinyin(region_name, style=Style.NORMAL)
        if len(words) > 0:
            self.region_py_name = "".join(map(str, [v.capitalize() for sub in words for v in sub]))

        # 自动设置区域类型
        region_type = {
            '0': REGION_TYPE_COUNTRY,
            '1': REGION_TYPE_PROVINCE,
            '2': REGION_TYPE_CITY,
            '3': REGION_TYPE_COUNTY,
        }
        if self.par_region:
            self.region_type = region_type.get(str(self.par_region.region_level + 1))
        else:
            self.region_type = region_type.get(str(self.region_level))
        # 保存
        super(CommonRegion, self).save()

    class Meta:
        db_table = 'common_region'
        verbose_name_plural = u'公共管理区域'
        verbose_name = u'公共管理区域'

    class MPTTMeta:
        parent_attr = 'par_region'
        level_attr = 'region_level'
        order_insertion_by = ['region_nbr']
