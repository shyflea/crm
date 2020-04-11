from django.urls import path

from common import views
from config.views.dictionary import DictionaryView

app_name = 'config'

urlpatterns = [
    path('dictionary/', DictionaryView.as_view()),  # 数据字典配置页面
    #path('commonregion/upload/', UploadCommonRegionView.as_view()),  # 导入区域配置
]
