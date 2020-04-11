from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from common.attrs import get_attr_values
from common.cache import read_from_cache, write_to_cache, CACHE_USER_PRIVS, CACHE_TIMEOUT_ONE_DAY
from common.constants import STATUS_ACTIVE, DEFAULT_MENU_ICON, PRIV_TYPE_FUNC, PRIV_REL_TYPE_MENU, MENU_TYPE_PAGE
from common.models import BaseModel
# Create your models here.
from ops.models.privilege import Privilege, PrivFuncRel


class FuncMenu(MPTTModel, BaseModel):
    menu_id = models.AutoField(primary_key=True, verbose_name='菜单标识')
    menu_name = models.CharField(max_length=50, db_index=True, verbose_name='菜单名称')
    menu_type = models.CharField(max_length=4, verbose_name='菜单类型', choices=get_attr_values('FuncMenu', 'MENU_TYPE'))
    menu_level = models.PositiveIntegerField(verbose_name='菜单级别', default=1)
    menu_index = models.PositiveIntegerField(verbose_name='菜单排序', default=1)
    par_menu = TreeForeignKey('self', on_delete=models.CASCADE, verbose_name='上级菜单',
                              blank=True, null=True, related_name='children')
    url_addr = models.CharField(max_length=250, verbose_name='菜单地址', blank=True)  # 菜单URL地址
    menu_desc = models.CharField(max_length=250, verbose_name='菜单描述', blank=True)
    icon = models.CharField(max_length=50, db_index=True, verbose_name='菜单图标', default=DEFAULT_MENU_ICON)

    def __str__(self):
        return u'%s' % self.menu_name

    class Meta:
        db_table = 'func_menu'
        verbose_name_plural = "菜单"  # 复数形式，如果只设置verbose_name，在Admin会显示为“菜单s”
        verbose_name = "菜单"
        ordering = ('menu_index',)

    class MPTTMeta:
        parent_attr = 'par_menu'
        level_attr = 'menu_level'

    # 获取菜单
    @classmethod
    def get_menus(self, user):
        # 先从缓存中取
        cache_key = CACHE_USER_PRIVS % user.sys_user_id
        menus = read_from_cache(cache_key)
        if menus:
            return menus
        # 取不到再查
        menus = []
        par_menus = self.objects.filter(par_menu_id=None, status_cd=STATUS_ACTIVE).order_by('menu_index')
        if len(par_menus) > 0:
            for menu in par_menus:
                # 判断是否有目录权限
                if user.has_perm_by_priv_id(menu.menu_id) is False:
                    continue
                # 添加目录
                child_datas = []
                par_data = {'name': menu.menu_name, 'icon': menu.icon, 'models': child_datas}
                menus.append(par_data)
                # 添加菜单
                childs = menu.children.filter(status_cd=STATUS_ACTIVE).order_by('menu_index')
                if len(childs) > 0:
                    for child in childs:
                        # 判断是否有菜单权限
                        if user.has_perm_by_priv_id(child.menu_id) is False:
                            continue
                        child_data = {'name': child.menu_name, 'url': child.url_addr, 'icon': child.icon}
                        child_datas.append(child_data)
        write_to_cache(cache_key, menus, CACHE_TIMEOUT_ONE_DAY)
        return menus

    # 获取权限编码
    def get_priv_code(menu_id):
        priv_code = None
        priv_func_rel = PrivFuncRel.objects.filter(priv_ref_id=menu_id, priv_ref_type=PRIV_REL_TYPE_MENU,
                                                   status_cd=STATUS_ACTIVE).first()
        if priv_func_rel and priv_func_rel.priv:
            priv_code = priv_func_rel.priv.priv_code
        return priv_code

    # 保存
    def save(self):
        # 保存功能菜单
        super(FuncMenu, self).save()
        privilege = None
        if self._state.adding is True:
            # 权限表
            privilege = Privilege()
            # 权限包含功能表
            priv_func_rel = PrivFuncRel()
        else:
            priv_func_rels = PrivFuncRel.objects.filter(priv_ref_id=self.menu_id, priv_ref_type=PRIV_REL_TYPE_MENU)
            if len(priv_func_rels) > 0:
                priv_func_rel = priv_func_rels[0]
                privilege = priv_func_rel.priv
            else:
                priv_func_rel = PrivFuncRel()
                privilege = Privilege()
        # 保存权限表
        privilege.priv_name = self.menu_name
        privilege.priv_type = PRIV_TYPE_FUNC
        # 当菜单为叶子节点（即页面时），设置编码跟django的权限编码对应上，
        if self.menu_type == MENU_TYPE_PAGE:
            url_addr = self.url_addr.split('/')
            privilege.priv_code = url_addr[0] + '.view_' + url_addr[1]
        privilege.save()
        # 保存权限包含功能表
        priv_func_rel.priv_id = privilege.priv_id
        priv_func_rel.priv_ref_id = self.menu_id
        priv_func_rel.priv_ref_type = PRIV_REL_TYPE_MENU
        priv_func_rel.save()
