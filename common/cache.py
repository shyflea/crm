import datetime
import json
import time

from django.conf import settings
from django.core.cache import cache

from common.constants import STATUS_ACTIVE, STATUS_INACTIVE
from log.models.cache_log import CacheLog

CACHE_ATTR_VALUES = 'ATTR_VALUES#%s#%s'  # 根据类名、属性编码获取属性值（元组）
CACHE_ATTR_DEFAULT_VALUE = 'ATTR_DEFAULT_VALUE#%s#%s'  # 根据类名、属性编码获取属性默认值
CACHE_ATTR_VALUE_NAME = 'ATTR_VALUE_NAME#%s#%s#%s'  # 根据类名、属性编码、属性值获取属性名称
CACHE_USER_PRIVS = 'USER_PRIVS#%d'  # 用户权限：根据sys_user_id区分

CACHE_TIMEOUT_DEFALUT = 7 * 24 * 60 * 60  # 缓存失效时间设置，默认七天
CACHE_TIMEOUT_ONE_DAY = 24 * 60 * 60  # 缓存失效时间设置，默认1天


def read_from_cache(key):
    """
    读取缓存
    :param key:
    :return:
    """
    value = cache.get(key)
    return value


def write_to_cache(key, value, timeout=None):
    """
    写进缓存
    :param key:
    :param value:
    :param timeout:
    :return:
    """
    if timeout is None:
        timeout = CACHE_TIMEOUT_DEFALUT
    cache.set(key, value, timeout)
    # 缓存记录到日志中
    if settings.CACHE_LOG_SAVE_IN_DB:
        from log.models.cache_log import CacheLog
        cache_log = CacheLog()
        cache_log.cache_key = key
        cache_log.cache_type = 'Redis'
        cache_log.cache_value = value
        cache_log.timeout = timeout
        cache_log.save()


def get_caches(pattern=None):
    """
    根据表达式查询所有符合的缓存，默认查询所有
    :return:
    """
    caches = {}
    if pattern is None:
        pattern = "*"
    else:
        pattern =  "*" + pattern + "*"
    keys = cache.keys(pattern)  # 查询所有Key
    if len(keys) > 0:

        for key in keys:  # 遍历Key，获取Value
            key_prefix = key.split('#')[0]
            index = 1
            values = []
            if key_prefix in caches:
                values = caches[key_prefix]
                index = len(values) + 1

            cache_key = get_cache_key(key_prefix, key[len(key_prefix) + 1:])
            cache_value = json.dumps(read_from_cache(key), ensure_ascii=False)
            cache_value = get_cache_value(key_prefix, cache_key, cache_value)
            eff_date = ''
            exp_date = ''
            cache_log = CacheLog.objects.filter(cache_key=key, status_cd=STATUS_ACTIVE).order_by(
                '-create_date').first()
            if cache_log:
                eff_date = datetime.datetime.strftime(cache_log.create_date, '%Y-%m-%d %H:%M:%S')
                exp_date = datetime.datetime.strftime(
                    cache_log.create_date + datetime.timedelta(seconds=cache_log.timeout), '%Y-%m-%d %H:%M:%S')
            value = {'index': index, 'key': key, 'value': cache_value, 'eff_date': eff_date, 'exp_date': exp_date,'cache_key': cache_key}
            values.append(value)
            caches[key_prefix] = values

    return caches


def delete_caches(pattern=None):
    """
    根据表达式删除缓存，默认删除所有
    :param pattern:
    :return:
    """
    # 表达式为空，则删除所有缓存
    if pattern is None:
        cache.clear()
        # 更新缓存日志
        if settings.CACHE_LOG_SAVE_IN_DB:
            CacheLog.objects.filter(status_cd=STATUS_ACTIVE). \
                update(status_cd=STATUS_INACTIVE,
                       update_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        # 表达式不为空，则删除指定缓存
        cache.delete_pattern(pattern + "*")
        # 更新缓存日志
        if settings.CACHE_LOG_SAVE_IN_DB:
            CacheLog.objects.filter(status_cd=STATUS_ACTIVE,cache_key__startswith=pattern). \
                update(status_cd=STATUS_INACTIVE,
                       update_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def get_cache_key(key_prefix, cache_key):
    """
    获取缓存对象,对一些缓存对象特殊处理，转换成用户可看懂的描述
    :param key_prefix:
    :param cache_key:
    :return:
    """
    # 用户权限缓存的缓存对象展示系统用户账号
    if key_prefix in CACHE_USER_PRIVS:
        from ops.models.system_user import SystemUser
        system_user = SystemUser.objects.get(sys_user_id=cache_key)
        return '%s ( %s )' % (system_user.sys_user_code, cache_key)
    return cache_key


def get_cache_value(key_prefix, cache_key, cache_value):
    """
    获取缓存值，对一些缓存值做特殊处理，转换成用户可看懂的描述
    :param key_prefix:
    :param cache_key:
    :param cache_value:
    :return:
    """
    #  属性默认值缓存的的属性值展示属性值名称
    if key_prefix in CACHE_ATTR_DEFAULT_VALUE:
        params = cache_key.split('#')
        from common.attrs import get_attr_value_name
        return '%s ( %s )' % (cache_value, get_attr_value_name(params[0], params[1], eval(cache_value)))
    return cache_value
