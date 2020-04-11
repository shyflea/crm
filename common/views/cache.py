from django.shortcuts import render
from django.views.generic import TemplateView

from common.cache import get_caches, delete_caches


class CacheView(TemplateView):
    template_name = 'admin/common/cache/cache.html'

    def post(self, request, *args, **kwargs):
        """
        删除缓存
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pattern = request.POST.get("cacheName")
        delete_caches(pattern)  # 删除缓存
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {}
        context['caches'] = get_caches()  # 查询缓存
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        """
         查询缓存
         :param request:
         :param args:
         :param kwargs:
         :return:
         """
        search_input = request.GET.get('searchInput')
        if search_input:
            search_input = search_input.strip()
        context = {}
        context['caches'] = get_caches(search_input)  # 查询缓存
        kwargs.update(context)
        context = super().get_context_data(**kwargs)
        return render(request, self.template_name, context)
