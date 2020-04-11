from django.contrib import admin

# Register your models here.
# 属性配置
from log.models.cache_log import CacheLog

admin.register(CacheLog)
