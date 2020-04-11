from django.contrib import admin
# Register your models here.
# Register your models here.
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from common.excel import ExportExcelMixin
from config.models.attr_spec import AttrSpec
from config.models.attr_value import AttrValue
from config.models.common_region import CommonRegion
from config.models.sys_class import SysClass
from config.models.sys_domain import SysDomain


# 区域配置
@admin.register(CommonRegion)
class CommonRegionAdmin(MPTTModelAdmin, ExportExcelMixin):
    list_display = ('region_name', 'region_py_name', 'region_nbr', 'region_type', 'province_nbr')  # 列表
    search_fields = ('region_name',)
    fieldsets = [(None, {'fields': ('region_name', 'region_nbr', 'par_region', 'province_nbr')})]
    actions = ['export_as_excel']  # 自定义动作
    # change_list_template = '/config/commonregion/mptt_change_list.html' mptt如果要重写的话要在这边设置模板路径


# 主题域配置
@admin.register(SysDomain)
class SysDomainAdmin(MPTTModelAdmin):
    list_display = ('domain_name', 'domain_nbr', 'domain_desc')  # 列表
    search_fields = ('domain_name', 'domain_nbr')
    fieldsets = [(None, {'fields': ('domain_name', 'domain_nbr', 'par_domain', 'domain_desc')})]


# 系统类配置
@admin.register(SysClass)
class SysClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_name', 'table_code', 'table_name', 'domain', 'oper')  # 列表
    search_fields = ('class_name', 'table_code')
    list_filter = ['domain']
    fieldsets = [(None, {'fields': ('class_name', 'table_code', 'table_name', 'domain')})]

    def oper(self, obj):
        # 参数名称和表字段名对应上，跳转到子页面，就可以自动添加上查询条件
        return mark_safe("<a href='/config/attrspec?sys_class_id=%d' target='_self'>属性</a>"
                         % obj.class_id)

    oper.short_description = '操作'


# 属性值配置
class AttrValueInline(admin.TabularInline):
    model = AttrValue
    fieldsets = [(None, {'fields': ('attr_value', 'attr_value_name', 'value_index')})]


# 属性配置
@admin.register(AttrSpec)
class AttrSpecAdmin(admin.ModelAdmin):
    list_display = ('attr_id', 'attr_nbr', 'attr_name', 'default_value', 'sys_class', 'status_name')  # 列表
    search_fields = ('attr_nbr', 'attr_name')
    list_filter = ['sys_class']
    fieldsets = [(None, {'fields': ('attr_nbr', 'attr_name', 'default_value', 'sys_class')})]
    list_display_links = ['attr_nbr', 'attr_name']
    inlines = [AttrValueInline]

