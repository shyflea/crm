from django.db import models
from mptt.fields import TreeForeignKey

from common.attrs import get_attr_values, get_attr_default_value
from common.models import BaseModel
from config.models.common_region import CommonRegion
from ops.models.organization import Organization


class Staff(BaseModel):
    staff_id = models.AutoField(primary_key=True, verbose_name='员工标识')
    staff_code = models.CharField(max_length=250, verbose_name='员工编号', null=True)
    staff_type = models.CharField(max_length=10, verbose_name='员工类型', choices=get_attr_values('Staff', 'STAFF_TYPE'),
                                  default=get_attr_default_value('Staff', 'STAFF_TYPE'))
    staff_name = models.CharField(max_length=250, verbose_name='员工姓名')
    org = TreeForeignKey(Organization, on_delete=models.CASCADE, verbose_name='隶属组织')
    region = TreeForeignKey(CommonRegion, on_delete=models.CASCADE, verbose_name='所在地区', null=True)

    class Meta:
        db_table = 'staff'
        verbose_name_plural = "员工"
        verbose_name = "员工"

    def __str__(self):
        return u'%s' % self.staff_name

    # 获取完整的区域名称
    def whole_region_name(self):
        region_name = ''
        if self.region:
            region_name = self.region.whole_region_name
        return region_name

    whole_region_name.short_description = u'所在区域'

    # 获取员工的系统用户
    def get_system_user(self):
        from ops.models.system_user import SystemUser
        systemuser = SystemUser.objects.filter(staff_id=self.staff_id).first()
        return systemuser

    # 系统用户任职岗位名称
    def post_name(self):
        system_user_post = self.get_system_user().get_system_user_post(self.org_id)
        if system_user_post is not None:
            return system_user_post.sys_post.sys_post_name
        return ''

    post_name.short_description = u'岗位'

    # 系统用户角色名称
    def role_name(self):
        name = ''
        system_user_roles = self.get_system_user().get_system_user_roles()
        if system_user_roles is None or len(system_user_roles) == 0:
            return name
        for system_user_role in system_user_roles:
            name = name + system_user_role.sys_role.sys_role_name + ','
        name = name.rstrip(',')
        return name

    role_name.short_description = u'角色'
