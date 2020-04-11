from common.cache import read_from_cache, write_to_cache, CACHE_ATTR_VALUES, CACHE_ATTR_DEFAULT_VALUE, \
    CACHE_ATTR_VALUE_NAME
from common.constants import STATUS_ACTIVE
from config.models.attr_spec import AttrSpec
from config.models.attr_value import AttrValue
from config.models.sys_class import SysClass


def get_attr_values(class_name, attr_nbr):
    """
    获取属性值
    在模型类的字段中给choices使用是，系统启动的时候会初始化
    :param class_name:类名
    :param attr_nbr:属性编码
    :return:属性列表
    """
    key = CACHE_ATTR_VALUES % (class_name, attr_nbr)
    # 从缓存中读取
    value = read_from_cache(key)
    if value:
        return value

    values = dict()
    attr_spec = get_attr_spec(class_name, attr_nbr)
    if attr_spec:
        # 获取属性下的所有生效的属性值
        attr_values = AttrValue.objects.filter(attr_id=attr_spec.attr_id, status_cd=STATUS_ACTIVE)
        if len(attr_values) > 0:
            for attr_value in attr_values:
                # 属性值-属性值名称
                values[attr_value.attr_value] = attr_value.attr_value_name
    value = tuple(items for items in values.items())
    # 写进缓存
    if value:
        write_to_cache(key, value)
    return value


def get_attr_default_value(class_name, attr_nbr):
    """
    获取属性默认值
    :param class_name:类名
    :param attr_nbr:属性编码
    :return:属性默认值
    """
    key = CACHE_ATTR_DEFAULT_VALUE % (class_name, attr_nbr)
    # 从缓存中读取
    deflaut_value = read_from_cache(key)
    if deflaut_value:
        return deflaut_value
    # 查数据库
    attr_spec = get_attr_spec(class_name, attr_nbr)
    if attr_spec:
        deflaut_value = attr_spec.default_value
    # 写进缓存
    if deflaut_value:
        write_to_cache(key, deflaut_value)
    return deflaut_value


# 获取属性
def get_attr_spec(class_name, attr_nbr):
    # 根据类名查系统类
    attr_spec = None
    sys_class = SysClass.objects.filter(class_name=class_name, status_cd=STATUS_ACTIVE).first()
    if sys_class:
        # 根据类ID、属性编码查属性
        attr_spec = AttrSpec.objects.filter(sys_class_id=sys_class.class_id, attr_nbr=attr_nbr,
                                            status_cd=STATUS_ACTIVE).first()
    return attr_spec


# 获取属性值名称
def get_attr_value_name(class_name, attr_nbr, attr_value):
    key = CACHE_ATTR_VALUE_NAME % (class_name, attr_nbr, attr_value)
    # 从缓存中读取
    attr_value_name = read_from_cache(key)
    if attr_value_name:
        return attr_value_name
    # 查数据库
    attr_spec = get_attr_spec(class_name, attr_nbr)
    if attr_spec:
        attr_value = AttrValue.objects.filter(attr_id=attr_spec.attr_id, status_cd=STATUS_ACTIVE,
                                              attr_value=attr_value).first()
        if attr_value:
            attr_value_name = attr_value.attr_value_name
        # 写进缓存
    if attr_value_name:
        write_to_cache(key, attr_value_name)
    return attr_value_name
