from django.urls import path

from ops.views.privilege import GrantPrivView, PrivConfigView, PrivilegeListView, PrivGrantListView, SystemPostView, \
    OrgPostSelfView, OrgPostView, SystemUserPostView, SystemRolesView, SystemUserRolesView

app_name = 'ops'

urlpatterns = [
    path('grant_priv/', GrantPrivView.as_view()),  # 授权页面
    path('get_all_privs/', PrivilegeListView.as_view()),  # 获取所有权限
    path('get_exist_privs/', PrivGrantListView.as_view()),  # 获取已拥有的权限，包括系统用户、系统岗位、系统角色三种类型
    path('save_grant/', GrantPrivView.as_view()),  # 保存用户权限
    path('get_all_post/', SystemPostView.as_view()),  # 获取所有岗位
    path('get_org_post_self/', OrgPostSelfView.as_view()),  # 获取组织自身配置的关联岗位
    path('get_org_post/', OrgPostView.as_view()),  # 获取组织所有关联岗位（如果自身未配置，则表示全部岗位都可支持)
    path('get_system_user_post/', SystemUserPostView.as_view()),  # 获取系统账号当前工号
    path('get_system_roles/', SystemRolesView.as_view()),  # 获取系统角色
    path('get_system_user_roles/', SystemUserRolesView.as_view()),  # 获取员工的系统角色
    path('priv_config/', PrivConfigView.as_view()),  # 权限配置页面
]
