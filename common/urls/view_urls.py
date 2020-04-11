from django.urls import path

from common.views import tools
from common.views.cache import CacheView

app_name = 'common'

urlpatterns = [
    path('pingyin/', tools.pingyin),  # 汉字转拼音
    path('cache/', CacheView.as_view()),  # 缓存
]
