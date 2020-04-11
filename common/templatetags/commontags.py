# -*- coding: utf-8 -*-

from django import template



register = template.Library()

# 获取参数
@register.simple_tag(takes_context=True)
def get_param(context, param):
    param_value = context.request.GET.get(param)
    return param_value

