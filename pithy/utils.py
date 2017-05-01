# coding=utf-8
import json
import time
import sys
from functools import wraps

python_version = sys.version[0]

if python_version == '3':
    basestring = str


def fn_timer(function):
    """
    元素查找计时器
    """
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        total_time = str(t1 - t0)
        return total_time, result

    return function_timer


def format_json(content):
    """
    格式化JSON
    """
    if isinstance(content, basestring):
        content = json.loads(content)

    if python_version == '3':
        result = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': ')). \
            encode('latin-1').decode('unicode_escape')
    else:
        result = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': ')). \
            decode("unicode_escape")

    return result


def pretty_print(content):
    """
    美化打印
    """
    print(format_json(content))
