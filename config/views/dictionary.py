from django.views.generic import TemplateView


class DictionaryView(TemplateView):
    template_name = 'admin/config/dictionary.html'

    # 页面初始化，跳转到数据字典配置页面
    def get_context_data(self, **kwargs):
        context = {
            'title':'数据字典'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
