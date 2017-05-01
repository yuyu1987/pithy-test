#!/usr/bin/python
# coding=utf-8
from requests.sessions import Session
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
from pprint import pprint
from copy import deepcopy
import json
import sys

from .utils import pretty_print
from .json_processor import JSONProcessor


def request(url='', method='get', data_type='json', interface_type='http', **request_kwargs):
    """
    使用方法：
        一、使用函数的方式组织
        @request(url='http://www.baidu.com', method='post', data_type='json')
        def get_baidu():
            pass

        二、使用类的方式组织(不指定session,指定base_url,不指定session的情况下,会自动为该类创建一个, )
        class TestBaidu(object):
            def __init(self):
                self.base_url = 'http://www.baidu.com'

            @request(url='')
            def test_get_baidu(self):
                pass

            @request(url='a'):
            def test_get_baidu2(self):
                pass

        三、使用类的方式组织(指定session,不指定base_url)
        class TestBaidu(object):
            def __init(self):
                self.session = None  # 也可以写成 sele.session = make_session()

            @request(url='http://www.baidu.com')
            def test_get_baidu(self):
                pass

    :param url: 要请求的域名
    :param method: http方法
    :param data_type: 请求的数据类型
    :param interface_type: 接口类型
    :param request_cookies: 请求的cookies
    :param request_files: 需上传的文件
    :param request_auth: 认证信息
    :param request_timeout: 超时时间
    :param request_verify: 是否需要验证证书
    :param request_stream:
    :param request_cert: 证书路径
    """
    request_data_name_list = ['request_cookies', 'request_files', 'request_auth', 'request_timeout',
                              'request_verify', 'request_stream', 'request_cert']

    # 剔除掉不支持的关键字参数
    for key in request_kwargs.keys():
        if key not in request_data_name_list:
            request_kwargs.pop(key)

    # 去掉'request_'前缀, 转换关键字参数为requests支持的格式
    for key in request_kwargs.keys():
        request_kwargs[key.split('_')[1]] = request_kwargs.pop(key)

    if str(method).lower() not in ['get', 'post', 'delete', 'put', 'patch', 'options', 'head']:
        raise TypeError(u'方法名输入不正确')

    request_kwargs['method'] = method

    if str(data_type).lower() not in ['json', 'form', None]:
        raise TypeError(u'data type传入不正确')

    def wrapper(f):
        """
        包含函数,接受函数对象
        """

        def wrapper_func(*args, **kwargs):
            """
            接收函数参数
            """

            def get_params(func, *args, **kwargs):
                """
                获取函数中定义的变量
                """
                get_params.locals = {}

                def tracer(frame, event, arg):
                    if event == 'return':
                        get_params.locals = frame.f_locals.copy()

                sys.setprofile(tracer)
                func(*args, **kwargs)
                params = get_params.locals
                get_params.locals = {}
                return params

            def create_url(data, variables_dict):
                """
                生成http请求的url
                """

                # 使用在函数中定义的url变量,如果没有,使用装饰器中定义的
                function_url = variables_dict.get('url') or url
                try:
                    base_url = getattr(variables_dict.get('self', None), 'base_url', '')
                except:
                    base_url = ''
                function_url = urljoin(base_url, function_url)

                # 校验url不能为空,且应包含http,弱校验
                if function_url and 'http' in function_url:
                    data['url'] = function_url
                else:
                    raise ValueError(u'url不能为空或url格式不正确,请加上协议名,如:http')

            def create_data(data, variables_dict):
                """
                生成请求的data,包含url参数和body参数
                """
                function_params = variables_dict.get('params')

                # 如果接口类型为http,取出用户定义的body,如为soa接口,组装soa body
                if interface_type == 'http':
                    function_body = variables_dict.get('body')
                else:
                    raise TypeError(u'不支持的类型')

                # 如果用户定义的body不为空,把body字典赋给data,对应requests参数里的data
                if function_body:
                    # 如果数据类型为json,dumps一下data
                    if data_type == 'json':
                        function_body = json.dumps(function_body)

                    data['data'] = function_body

                # 如果用户定义的params不为空,则赋给params,对应requests里的params
                if function_params:
                    data['params'] = function_params

            def create_headers(data, variables_dict):
                """
                生成头部信息
                """
                data['headers'] = {}
                function_headers = variables_dict.get('headers')

                # 如果用户定义的headers不为空,更新到headers
                if function_headers:
                    data['headers'].update(function_headers)

                # 根据data type的类型添加不同的头部信息
                if data_type == 'json':
                    data['headers'].update(
                        {"Accept": r"application/json, text/plain, */*",
                         "Content-Type": r"application/json"}
                    )
                elif data_type == 'form':
                    data['headers'].update(
                        {"Content-Type": r"application/x-www-form-urlencoded"}
                    )
                else:
                    pass

            def create_session(data, variables_dict):
                """
                如果接收到的要变参数中有session,且为Session对象,赋值给session变量, 否则创建一个
                """
                if 'self' in variables_dict:
                    try:
                        data['session'] = getattr(variables_dict.get('self', None), 'session')
                        if not isinstance(data['session'], Session):
                            session = Session()
                            setattr(variables_dict.get('self', None), 'session', session)
                            data['session'] = session
                    except Exception as e:
                        session = Session()
                        setattr(variables_dict.get('self', None), 'session', session)
                        data['session'] = session

                elif isinstance(variables_dict.get('session'), Session):
                    data['session'] = variables_dict.get('session')
                else:
                    data['session'] = Session()

            # 获取函数或方法内定义的变量
            data = deepcopy(request_kwargs)
            data['doc'] = f.__doc__ or f.__name__
            function_variables_dict = get_params(f, *args, **kwargs)

            # 如果函数方法内有定义参数,更新到data里
            for key in function_variables_dict.keys():
                if key in request_data_name_list:
                    data[key.split('_')[1]] = function_variables_dict[key]

            create_url(data, function_variables_dict)
            create_data(data, function_variables_dict)
            create_headers(data, function_variables_dict)
            create_session(data, function_variables_dict)
            return Request(data)

        return wrapper_func

    return wrapper


class Request(object):
    """
    请求对象模型
    """

    def __init__(self, data):
        self.session = data.pop('session')
        self.method = data.pop('method')
        self.url = data.pop('url')
        self.interface_doc = data.pop('doc')
        self.data = data
        self.num = 4
        self.response = None

    def to_json(self):
        self._request()
        try:
            response_json = self.response.json()
            print('')
            print(u'{num} 响应结果:'.format(num=self.num))
            pretty_print(response_json)
        except ValueError:
            print(u"调用接口失败,状态码为:{status_code}".format(status_code=self.response.status_code))
            print(self.response.content)
            raise ValueError('No JSON object in response')

        return JSONProcessor(response_json)

    def to_content(self):
        self._request()
        response_content = self.response.content
        print('')
        print(u'{num} 响应结果:'.format(num=self.num))
        print(response_content)
        return response_content

    def get_cookie(self):
        self._request()
        cookies = dict(self.response.cookies)
        print('')
        print(u'{num} 响应cookies:'.format(num=self.num))
        print('')
        pprint(cookies)
        return cookies

    @property
    def json(self):
        return self.to_json()

    @property
    def content(self):
        return self.to_content()

    @property
    def cookie(self):
        return self.get_cookie()

    def _request(self):
        if not self.response:
            self._print_request_data()
            self.response = self.session.request(self.method, self.url, **self.data)

    def _print_request_data(self):
        print('')
        print('******************************************************')
        print('')
        print(u'1 接口描述:')
        print(self.interface_doc)
        print('')
        print(u'2 请求url')
        print('url: {url}'.format(url=self.url))
        print('')
        print(u'3 请求方法')
        print(u'method: {method}'.format(method=self.method))
        self.session.headers.update(self.data.get('headers'))

        if self.session.headers:
            print('')
            print(u'{num} 请求headers:'.format(num=self.num))
            self.num += 1
            pretty_print(dict(self.session.headers))

        if self.data.get('params'):
            print('')
            print(u'{num} 请求url参数:'.format(num=self.num))
            self.num += 1
            pretty_print(self.data.get('params'))

        if self.data.get('data'):
            print('')
            print(u'{num} 请求body参数:'.format(num=self.num))
            self.num += 1
            pretty_print(self.data.get('data'))

    def __getattr__(self, item):
        self._request()
        return getattr(self.response, item)


def make_session():
    return Session()
