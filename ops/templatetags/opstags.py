# -*- coding: utf-8 -*-

import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from django.utils.functional import Promise

from ops.models.func_menu import FuncMenu

register = template.Library()


# 获取菜单
@register.simple_tag(takes_context=True)
def my_menus(context, _get_config=None):
    user = context.request.user
    data = FuncMenu.get_menus(user)
    return '<script type="text/javascript">var menus={}</script>'.format(json.dumps(data, cls=LazyEncoder))


class LazyEncoder(DjangoJSONEncoder):
    """
        解决json __proxy__ 问题
    """

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)
