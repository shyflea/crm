from django.contrib import admin
from django.urls import path, include

from crm import error_views

admin.site.site_title = '客户关系管理系统'
admin.site.site_header = '客户关系管理系统'

# api
api = [
    path('config/', include('config.urls.api_urls', namespace='api-config')),
    path('ops/', include('ops.urls.api_urls', namespace='api-ops')),
]

# 入口
urlpatterns = [
    path('', admin.site.urls),
    path('api/', include(api)),
]

# 应用视图
app_view_patterns = [
    path('common/', include('common.urls.view_urls', namespace='common')),
    path('config/', include('config.urls.view_urls', namespace='config')),
    path('ops/', include('ops.urls.view_urls', namespace='ops')),
]
urlpatterns += app_view_patterns



# 自定义错误处理页面 settting 中 debug 要设置成false
handler404 = error_views.handler404
handler500 = error_views.handler500
