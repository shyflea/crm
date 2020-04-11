from django.db import models

from common.constants import STATUS_ACTIVE

# Create your models here.
class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_date = models.DateTimeField(auto_now=True)  # 修改时间
    status_cd = models.CharField(max_length=4, verbose_name='状态', default=STATUS_ACTIVE)

    class Meta:
        abstract = True     # 抽象基类，不生成单独数据表

    # 状态名称
    def status_name(self):
        from common.attrs import get_attr_value_name
        return get_attr_value_name('BaseModel','STATUS_CD',self.status_cd)
    status_name.short_description = u'状态'
