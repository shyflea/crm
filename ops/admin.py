from django.contrib import admin
# Register your models here.
from django.forms import BaseInlineFormSet
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from common.constants import STATUS_ACTIVE, GRANT_OBJ_TYPE_SYSTEM_POST, GRANT_OBJ_TYPE_SYSTEM_ROLES, \
    GRANT_OBJ_TYPE_SYSTEM_USER
from common.utils import make_md5
from ops.models.func_menu import FuncMenu
from ops.models.organization import Organization, OrgPostRel
from ops.models.privilege import Privilege, PrivGrant
from ops.models.staff import Staff
from ops.models.system_post import SystemPost
from ops.models.system_roles import SystemRoles
from ops.models.system_user import SystemUser


# 菜单管理
@admin.register(FuncMenu)
class FuncMenuAdmin(MPTTModelAdmin):
    list_display = ('menu_name', 'menu_type', 'url_addr', 'menu_index')  # 列表
    # list_editable 设置默认可编辑字段
    list_editable = ['menu_index']
    # 查询条件
    search_fields = ('menu_name',)  # 主查询条件
    list_filter = ['menu_type']  # 其他筛选条件
    # 编辑页采集信息
    fieldsets = [(None, {'fields': ('menu_name', 'menu_type', 'par_menu', 'menu_index', 'url_addr', 'icon')})]


# 组织管理
@admin.register(Organization)
class OrganizationAdmin(MPTTModelAdmin):
    list_display = ('org_name', 'org_type', 'org_level', 'region')  # 列表
    search_fields = ('org_name',)
    fieldsets = [('组织信息', {'fields': ('org_name', 'org_type', 'parent_org', 'region', 'org_index')})]

    # 编辑页面初始化
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # 获取组织已拥有的岗位需要用到org_id，因此在页面加载的时候需要先预留
        if object_id:
            extra_context = {'org_id': object_id}
        return super().change_view(request, object_id, form_url, extra_context)

    # 保存模型
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        posts = request.POST.get('posts')
        post_list = []
        if posts:
            post_list = str(posts).split(',')
        if len(post_list) > 0:
            # 删除岗位
            OrgPostRel.objects.filter(org_id=obj.org_id, status_cd=STATUS_ACTIVE).exclude(
                sys_post_id__in=post_list).delete()
            # 增加
            for sys_post_id in post_list:
                org_post_rel = OrgPostRel.objects.filter(org_id=obj.org_id, status_cd=STATUS_ACTIVE,
                                                         sys_post_id=sys_post_id)
                if org_post_rel is None or len(org_post_rel) == 0:
                    org_post_rel = OrgPostRel()
                    org_post_rel.org_id = obj.org_id
                    org_post_rel.sys_post_id = sys_post_id
                    org_post_rel.save()
        else:
            # 没有选择的岗位的情况下，将所有岗位删除
            OrgPostRel.objects.filter(org_id=obj.org_id, status_cd=STATUS_ACTIVE).delete()


# # 系统用户
class SystemUserFormset(BaseInlineFormSet):
    # 新增时保存
    def save_new(self, form, commit=True):
        obj = super(SystemUserFormset, self).save_new(form, commit=False)
        # 初始化密码为系统账号
        if not obj.password:
            obj.password = make_md5(obj.sys_user_code)

        if commit:
            obj.save()
            post = self.data.get('post')
            org_id = self.data.get('org')
            roles = self.data.get('roles')
            obj.save_post_and_role(org_id, post, roles)
        return obj


class SystemUserInline(admin.TabularInline):
    model = SystemUser
    formset = SystemUserFormset

    fieldsets = [('系统用户', {
        'fields': ('sys_user_code', 'pwd_err_cnt', 'pwd_sms_tel', 'pwd_effect_days')})]


# 员工管理
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    inlines = [SystemUserInline]  # Inline
    # 列表展示
    list_display = (
        'staff_name', 'staff_code', 'staff_type', 'org', 'post_name', 'role_name', 'whole_region_name', 'oper')
    # 查询条件
    search_fields = ('staff_name', 'staff_code')
    list_filter = ['org', 'staff_type']
    # 编辑页展示信息
    fieldsets = (['员工信息', {'fields': ('staff_name', 'staff_code', 'staff_type', 'org', 'region')}],)

    # 编辑页面初始化
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # 获取组织已拥有的岗位需要用到org_id，因此在页面加载的时候需要先预留
        if object_id:
            extra_context = {'staff_id': object_id}
        return super().change_view(request, object_id, form_url, extra_context)

    # 保存模型
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change is True:
            obj.get_system_user().save_post_and_role(obj.org_id, request.POST.get("post"), request.POST.get("roles"))

    def oper(self, obj):
        return mark_safe("<a href='/ops/grant_priv?grant_obj_id=%d&grant_obj_type=%s' target='_self'>授权</a>"
                         % (obj.get_system_user().sys_user_id, GRANT_OBJ_TYPE_SYSTEM_USER))

    oper.short_description = '操作'


# 权限管理
@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('priv_name', 'priv_code', 'priv_type')  # 列表
    search_fields = ('priv_name', 'priv_code')
    fieldsets = [(None, {'fields': ('priv_name', 'priv_code', 'priv_type', 'priv_desc')})]


# 角色管理
@admin.register(SystemRoles)
class SystemRolesAdmin(admin.ModelAdmin):
    list_display = ('sys_role_name', 'sys_role_code', 'init_flag', 'sys_role_desc', 'oper')  # 列表
    search_fields = ('sys_role_name',)
    fieldsets = [(None, {'fields': ('sys_role_name', 'sys_role_code', 'init_flag', 'sys_role_desc')})]

    def oper(self, obj):
        return mark_safe("<a href='/ops/grant_priv?grant_obj_id=%d&grant_obj_type=%s' target='_self'>授权</a>"
                         % (obj.sys_role_id, GRANT_OBJ_TYPE_SYSTEM_ROLES))

    oper.short_description = '操作'


# 岗位管理
@admin.register(SystemPost)
class SystemPostAdmin(admin.ModelAdmin):
    list_display = ('sys_post_name', 'sys_post_code', 'init_flag', 'sys_post_desc', 'oper')  # 列表
    search_fields = ('sys_post_name',)
    fieldsets = [(None, {'fields': ('sys_post_name', 'sys_post_code', 'init_flag', 'sys_post_desc')})]

    def oper(self, obj):
        return mark_safe("<a href='/ops/grant_priv?grant_obj_id=%d&grant_obj_type=%s' target='_self'>授权</a>"
                         % (obj.sys_post_id, GRANT_OBJ_TYPE_SYSTEM_POST))

    oper.short_description = '操作'


# 授权管理
@admin.register(PrivGrant)
class PrivGrantAdmin(admin.ModelAdmin):
    list_display = ('priv', 'oper_type', 'grant_obj_type', 'grant_obj',)  # 列表
    search_fields = ('priv', 'grant_obj_id',)
    fieldsets = [(None, {'fields': ('priv', 'oper_type', 'grant_obj_type', 'grant_obj_id',)})]

