from django.db import models

from common.models import BaseModel


class CacheLog(BaseModel):
    """
     缓存日志
    """
    log_id = models.AutoField(primary_key=True, verbose_name='日志标志')
    cache_type = models.CharField(max_length=30, verbose_name='缓存类型', db_index=True)
    cache_key = models.CharField(max_length=250, verbose_name='缓存key', db_index=True)
    cache_value = models.TextField(verbose_name='缓存值', null=True, blank=True)
    timeout = models.IntegerField(verbose_name='缓存失效时间')

    def __str__(self):
        return u'%s' % self.cache_key

    class Meta:
        db_table = 'cache_log'
        verbose_name_plural = "缓存日志"
        verbose_name = "缓存日志"
