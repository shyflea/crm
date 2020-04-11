import hashlib

from pypinyin import pinyin, Style


# 汉字转拼英
def trans_to_pingyin(chinese):
    content = ''
    words = pinyin(chinese, style=Style.NORMAL)
    if len(words) > 0:
        content = "".join(map(str, [v for sub in words for v in sub]))
    return content


# md5加密
def make_md5(password):
    md5 = hashlib.md5()
    # 实例化md5加密方法
    md5.update(password.encode())
    # 进行加密，python2可以给字符串加密，python3只能给字节加密
    return md5.hexdigest()


# 将文字的编码转换成中文编码
def trans_to_chinese_code(str):
    if not str or str == '':
        return ''
    return str.encode('utf-8').decode('ISO-8859-1')
