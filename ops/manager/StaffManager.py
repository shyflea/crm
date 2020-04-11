from django.contrib.auth.base_user import BaseUserManager

# 重写UserManager
from django.db import transaction

from common.utils import make_md5
from config.models.common_region import CommonRegion
from ops.models.staff import Staff


class StaffManager(BaseUserManager):
    use_in_migrations = True

    @transaction.atomic
    def _create_staff(self, sys_user_code, password, **extra_fields):
        if not sys_user_code:
            raise ValueError("请填入账号！")
        if not password:
            raise ValueError("请填入密码！")
        # 组织
        from ops.models.organization import Organization
        org = Organization.objects.filter(org_id=1)
        if len(org) == 0:
            org = Organization()
            org.org_name = '默认团队'
            org.save()

        # 区域
        region = CommonRegion.objects.filter(common_region_id=1)
        if len(region) == 0:
            region = CommonRegion()
            region.region_name = '中国'
            region.save()

        # 员工
        staff = Staff()
        staff.staff_name = sys_user_code
        staff.region_id = region.common_region_id
        staff.org_id = org.org_id
        staff.save()
        # 系统账号
        from ops.models.system_user import SystemUser
        system_user = SystemUser(**extra_fields)
        system_user.sys_user_code = sys_user_code
        system_user.password = make_md5(password)
        system_user.staff_id = staff.staff_id
        system_user.save()

        return system_user

    def create_user(self, sys_user_code, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(sys_user_code, password, **extra_fields)

    def create_superuser(self, sys_user_code, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_staff(sys_user_code, password, **extra_fields)
