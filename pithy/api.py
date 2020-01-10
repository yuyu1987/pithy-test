#!/usr/bin/python
# coding=utf-8
import logging
from requests.sessions import Session
from functools import wraps
from jinja2 import Template
from copy import deepcopy
from collections import OrderedDict
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
import inspect

from .utils import format_json
from .json_processor import JSONProcessor


class HttpRequest(object):
    def __init__(self, url='', method='get', **kwargs):
        self.url = url
        self.method = method
        self.decorator_args = kwargs
        self.func_return = None
        self.func_doc = None
        self.func_im_self = None
        self.session = None

    def __call__(self, func):
        self.func = func
        self.is_class = False
        try:
            if inspect.getfullargspec(func).args[0] == 'self':
                self.is_class = True
        except IndexError:
            pass

        def fun_wrapper(*args, **kwargs):
            self.func_return = self.func(*args, **kwargs) or {}
            self.func_im_self = args[0] if self.is_class else object

            try:
                self.func.__doc__ = self.func.__doc__.decode('utf-8')
            except:
                pass
            self.func_doc = (self.func.__doc__ or self.func.__name__).strip()
            self.create_url()
            self.create_session()
            self.session.headers.update(getattr(self.func_im_self, 'headers', {}))
            self.decorator_args.update(self.func_return)
            return Request(self.method, self.url, self.session, self.func_doc, self.decorator_args)
        return fun_wrapper

    def create_url(self):
        """
        生成http请求的url
        """

        # 使用在函数中定义的url变量,如果没有,使用装饰器中定义的
        base_url = getattr(self.func_im_self, 'base_url', '')
        self.url = self.func_return.pop('url', None) or self.url
        self.url = urljoin(base_url, self.url)

    def create_session(self):
        """
        如果接收到的要变参数中有session,且为Session对象,赋值给session变量, 否则创建一个
        """
        if self.is_class:
            self.session = getattr(self.func_im_self, 'session', None)
            if not isinstance(self.session, Session):
                session = Session()
                setattr(self.func_im_self, 'session', session)
                self.session = session

        elif isinstance(self.func_return.get('session'), Session):
            self.session = self.func_return.get('session')
        else:
            self.session = Session()


request = HttpRequest

LOG_TEMPLATE = u'''
******************************************************
{% for index, item in items %}
{{ index + 1 }}、{{ item['desc'] }}
{{ item['value'] }}
{% endfor %}
'''


def context(func):
    def wrapper(self):
        self._request()
        try:
            res = func(self)
        finally:
            self._log()
        return res
    return wrapper


class Request(object):
    """
    请求对象模型
    """

    def __init__(self, method, url, session, doc, args):
        self.method = method
        self.url = url
        self.session = session
        self.doc = doc
        self.args = args
        self.response = None
        self.log_content = [
            dict(desc=u'接口描述', value=doc),
            dict(desc=u'请求url', value=url),
            dict(desc=u'请求方法', value=method),
        ]

        for i in ['params', 'data']:
            if args.get(i):
                args[i] = self.fixation_order(args[i])

    def get_arg(self, arg):
        return self.args.get(arg)

    def add_headers(self, **kwargs):
        if self.args.get('headers'):
            self.args['headers'].update(kwargs)
        else:
            self.args['headers'] = kwargs

    @staticmethod
    def fixation_order(d):
        o = OrderedDict()
        for i in d:
            o[i] = d[i]
        return o

    def prepare_log(self):
        headers = deepcopy(self.args.get('headers', {}))
        headers.update(self.session.headers)

        if headers:
            self.log_content.append(dict(
                desc=u'请求headers', value=format_json(headers)
            ))

        if self.args.get('params'):
            self.log_content.append(dict(
                desc=u'请求url参数', value=format_json(self.args.get('params'))
            ))

        if self.args.get('data'):
            self.log_content.append(dict(
                desc=u'body参数', value=format_json(self.args.get('data'))
            ))

        if self.args.get('json'):
            self.log_content.append(dict(
                desc=u'body参数', value=format_json(self.args.get('json'))
            ))

    @context
    def to_json(self):
        try:
            response_json = self.response.json()
            self.log_content.append(dict(
                desc=u'响应结果',
                value=format_json(response_json)
            ))
        except ValueError:
            self.log_content.append(dict(
                desc=u'响应结果',
                value=self.response.content.decode('utf-8')
            ))
            raise ValueError(u'No JSON object in response')

        return JSONProcessor(response_json)

    @context
    def to_content(self):
        response_content = self.response.content
        self.log_content.append(dict(desc=u'响应结果', value=response_content.decode('utf-8')))
        return response_content

    @property
    def json(self):
        return self.to_json()

    @property
    def content(self):
        return self.to_content()

    def _log(self):
        print(Template(LOG_TEMPLATE).render(items=enumerate(self.log_content)))

    def _request(self):
        if not self.response:
            self.prepare_log()
            self.response = self.session.request(self.method, self.url, **self.args)

    def __getattr__(self, item):
        self._request()
        self._log()
        return getattr(self.response, item)


def make_session():
    return Session()


class response(Request):
    def __new__(cls, **kwargs):
        """
        :rtype: Request
        """
        return dict(**kwargs)
