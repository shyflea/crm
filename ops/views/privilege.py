import json
import traceback

from django.http import HttpResponse
from django.views.generic import TemplateView

from common.constants import STATUS_ACTIVE, GRANT_OBJ_TYPE_SYSTEM_USER, TRUE, FALSE, GRANT_OBJ_TYPE_SYSTEM_POST, \
    GRANT_OBJ_TYPE_SYSTEM_ROLES
from common.utils import trans_to_pingyin
from ops.models.organization import OrgPostRel
from ops.models.privilege import Privilege, PrivGrant
from ops.models.system_post import SystemPost
from ops.models.system_roles import SystemRoles
from ops.models.system_user import SystemUser, SystemUserPost

__all__ = [
    'PrivConfigView', 'GrantPrivView', 'PrivilegeListView', 'PrivGrantListView', 'SystemPostView', 'OrgPostSelfView',
    'OrgPostView', 'SystemUserPostView', 'SystemRolesView', 'SystemUserRolesView', 'PrivConfigView'
]


# 权限管理页面
class PrivConfigView(TemplateView):
    template_name = 'admin/ops/priv_config.html'


# 授权配置页面
class GrantPrivView(TemplateView):
    template_name = 'admin/ops/grant_priv.html';

    # 页面初始化，跳转到授权页面
    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = '授权'
        # 设置授权对象和授权类型
        context['grant_obj_id'] = self.request.GET.get('grant_obj_id')
        grant_obj_type = self.request.GET.get('grant_obj_type')
        context['grant_obj_type'] = grant_obj_type
        # 设置主页面，用于返回上一页
        context['main_url'] = get_grant_main_url(grant_obj_type)
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    # 保存系统用户权限
    def post(self, request, *args, **kwargs):
        respond = None
        try:
            priv_ids = request.POST.getlist("priv_ids[]")
            grant_obj_id = request.POST.get("grant_obj_id")
            grant_obj_type = request.POST.get("grant_obj_type")

            # 查询授权对象拥有的权限
            priv_grants = PrivGrant.get_priv_grants(grant_obj_id, grant_obj_type)
            # 删除回收的授权规则
            if len(priv_grants) > 0:
                for priv_grant in priv_grants:
                    if len(priv_ids) == 0:  # 如果授权已清空，则将原来所有的授权都删除；
                        priv_grant.delete()
                    elif priv_grant.priv_id not in priv_ids:  # 如果原来的授权已不在授权列表中，也要删除
                        priv_grant.delete()
            # 新增授权
            if len(priv_ids) > 0:
                # 系统用户权限
                if grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_USER:
                    user = SystemUser.objects.get(sys_user_id=grant_obj_id)
                    for priv_id in priv_ids:
                        if user.has_perm_by_priv_id(priv_id) is False:  # 系统用户除了判断自身有无权限，还需要判断角色、岗位上有没有权限
                            PrivGrant.add_priv_grant(priv_id, grant_obj_id, grant_obj_type)
                elif grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_POST or grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_ROLES:  # 系统岗位权限 和 系统角色权限
                    for priv_id in priv_ids:
                        add = True
                        if len(priv_grants) == 0:  # 原来没有授权，则直接新增
                            add = True
                        else:
                            for priv_grant in priv_grants:  # 原来有授权的，需要判断现在新增的授权有没有在其中
                                if priv_id == priv_grant.priv_id:
                                    add = True
                                    break
                        if add is True:
                            PrivGrant.add_priv_grant(priv_id, grant_obj_id, grant_obj_type)

            # 返回页面
            response = {'status': TRUE, 'url': get_grant_main_url(grant_obj_type)}

        except Exception as e:
            traceback.print_exc()
            response = {'status': FALSE, 'msg': '保存失败!'}

        return HttpResponse(json.dumps(response), content_type='application/json')


# 获取授权主页面地址（员工管理、岗位管理、角色管理）
def get_grant_main_url(grant_obj_type):
    url = ''
    if grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_USER:
        url = '/ops/staff/'
    elif grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_POST:  # 系统岗位权限
        url = '/ops/systempost/'
    elif grant_obj_type == GRANT_OBJ_TYPE_SYSTEM_ROLES:  # 系统角色权限
        url = '/ops/systemroles/'
    return url


class PrivilegeListView(TemplateView):
    # 获取所有权限
    def get(self, request, *args, **kwargs):
        privs = Privilege.objects.filter(status_cd=STATUS_ACTIVE)
        content = json.dumps(self.trans_to_transfer_data(privs))  #
        return HttpResponse(content, "application/json")

    # 权限转成供穿梭框展示的数据结构
    def trans_to_transfer_data(slef, privs):
        datas = []
        for privilege in privs:
            data = {
                'key': privilege.priv_id,
                'label': privilege.priv_name,
                'pingyin': trans_to_pingyin(privilege.priv_name)
            }
            datas.append(data)
        return datas


class PrivGrantListView(TemplateView):
    # 获取已拥有的权限，包括系统用户、系统岗位、系统角色三种类型
    def get(self, request, *args, **kwargs):
        priv_ids = []  # 返回的权限id

        grant_obj_id = request.GET.get("grant_obj_id")
        grant_obj_type = request.GET.get("grant_obj_type")
        # 查询授权规则
        priv_grants = PrivGrant.get_priv_grants(grant_obj_id, grant_obj_type)
        if len(priv_grants) > 0:
            for priv_grant in priv_grants:
                priv_ids.append(priv_grant.priv_id)

        content = json.dumps(priv_ids)
        return HttpResponse(content, "application/json")


class SystemPostView(TemplateView):

    # 获取所有岗位
    def get(self, request, *args, **kwargs):
        posts = SystemPost.objects.filter(status_cd=STATUS_ACTIVE)
        datas = []
        for post in posts:
            data = {
                'key': post.sys_post_id,
                'label': post.sys_post_name,
                'pingyin': trans_to_pingyin(post.sys_post_name)
            }
            datas.append(data)
        return HttpResponse(json.dumps(datas), "application/json")


class OrgPostSelfView(TemplateView):
    # 获取组织自身配置的关联岗位
    def get(self, request, *args, **kwargs):
        post_ids = []
        org_id = request.GET.get("org_id")
        if org_id:
            org_post_rels = OrgPostRel.objects.filter(org_id=org_id, status_cd=STATUS_ACTIVE)
            if len(org_post_rels) > 0:
                for org_post_rel in org_post_rels:
                    post_ids.append(org_post_rel.sys_post_id)

        content = json.dumps(post_ids)
        return HttpResponse(content, "application/json")


class OrgPostView(TemplateView):
    # 获取组织拥有的岗位
    def get(self, request, *args, **kwargs):
        system_posts = []
        org_id = request.GET.get("org_id")
        org_post_rels = OrgPostRel.objects.filter(org_id=org_id, status_cd=STATUS_ACTIVE)
        if len(org_post_rels) > 0:
            for org_post_rel in org_post_rels:
                system_posts.append(org_post_rel.sys_post)
        else:
            system_posts = SystemPost.objects.filter(status_cd=STATUS_ACTIVE)
        posts = []
        if len(system_posts) > 0:
            for system_post in system_posts:
                post = {}
                post['sys_post_id'] = system_post.sys_post_id
                post['sys_post_name'] = system_post.sys_post_name
                posts.append(post)
        content = json.dumps(posts)
        return HttpResponse(content, "application/json")


class SystemUserPostView(TemplateView):
    # 获取员工拥有的岗位
    def get(self, request, *args, **kwargs):
        sys_post_id = ''
        staff_id = request.GET.get("staff_id")
        if staff_id:
            system_user = SystemUser.objects.filter(staff_id=staff_id, status_cd=STATUS_ACTIVE).first()
            if system_user:
                system_user_post = SystemUserPost.objects.filter(sys_user_id=system_user.sys_user_id,
                                                                 status_cd=STATUS_ACTIVE).first()
                if system_user_post:
                    sys_post_id = system_user_post.sys_post_id
        return HttpResponse(sys_post_id)


class SystemRolesView(TemplateView):
    # 获取系统角色
    def get(self, request, *args, **kwargs):
        roles = []
        system_roles = SystemRoles.objects.filter(status_cd=STATUS_ACTIVE)
        if len(system_roles) > 0:
            for system_role in system_roles:
                role = {}
                role['sys_role_name'] = system_role.sys_role_name
                role['sys_role_id'] = system_role.sys_role_id

                roles.append(role)
        content = json.dumps(roles)
        return HttpResponse(content, "application/json")


class SystemUserRolesView(TemplateView):
    # 获取员工的系统角色
    def get(self, request, *args, **kwargs):
        roles = []
        staff_id = request.GET.get("staff_id")
        if staff_id:
            system_user_roles = SystemUser.get_system_user_roles_by_staff_id(staff_id)
            if len(system_user_roles) > 0:
                for system_user_role in system_user_roles:
                    roles.append(system_user_role.sys_role.sys_role_name)
        content = json.dumps(roles)
        return HttpResponse(content, "application/json")
