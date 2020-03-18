# coding:utf-8

import re
import hashlib
from datetime import datetime

def time_now():
    return datetime.isoformat(datetime.now(), sep=' ')

def time_find(arg):
    _now = datetime.today()
    t = re.compile('(\d+)\w+?|[0-9:]{5}\w+?')
    if '天' in arg:
        day = t.search(arg).group(1)
        _now.day = _now.day - day
    elif '月' in arg:
        month = t.search(arg).group(1)
        _now.month = _now.month - month
    else:
        hour, min = t.search(arg).group(1).split(':')
        _now.hour = hour
        _now.minute = min
    return datetime.isoformat((_now.year, _now.month, _now.day, _now.hour, _now.minute, _now.second, 0), sep=' ')


def get_string(select="", payload="", join=False):
    result = select.xpath(payload).extract()
    if result:
        if join:
            result = "".join(result).strip()
        else:
            result = result[0]
    else:
        result = ''
    return result


def create_md5(url):
    if not url:
        return ''
    result = hashlib.md5()
    result.update(url.encode('utf8'))
    return result.hexdigest()