快速开始
======================================

--------------------------------------

生成测试项目
--------------------------------------

查看使用方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> pithy-cli
    Usage: pithy-cli [OPTIONS] COMMAND [ARGS]...

    pithy-cli是一个接口测试项目生成脚手架,功能完善中

    Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

    Commands:
    init  生成接口测试项目 使用方法: $ pithy-cli init # 生成接口测试项目

生成测试项目
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> pithy-cli init
    请选择项目类型,输入api或者app: api
    请输入项目名称,如pithy-api-test: pithy-api-test
    开始创建pithy-api-test项目
    开始渲染...
    生成 api/.gitignore                   [√]
    生成 api/apis/__init__.py             [√]
    生成 api/apis/pithy_api.py            [√]
    生成 api/cfg.yaml                     [√]
    生成 api/db/__init__.py               [√]
    生成 api/db/pithy_db.py               [√]
    生成 api/README.MD                    [√]
    生成 api/requirements.txt             [√]
    生成 api/test_suites/__init__.py      [√]
    生成 api/test_suites/test_login.py    [√]
    生成 api/utils/__init__.py            [√]
    生成成功,请使用编辑器打开该项目

.. attention::
  app还未开发，暂时还不能生成


生成的项目结构
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    >>> tree pithy-api-test
    pithy-api-test
    ├── README.MD
    ├── apis
    │   ├── __init__.py
    │   └── pithy_api.py
    ├── cfg.yaml
    ├── db
    │   ├── __init__.py
    │   └── pithy_db.py
    ├── requirements.txt
    ├── test_suites
    │   ├── __init__.py
    │   └── test_login.py
    └── utils
        └── __init__.py

    4 directories, 10 files

HTTP API测试
--------------------------------------
这个地方对python requests进行了封装，在原api不变的基础上，把原先的语句调用方式，扩展成了函数定义，然后对输出进行了包装，下面对比一下两种写法的不同

::

    import requests
    from pithy import request

    # 直接使用requets的api
    data = {'key': 'value'}
    requests.get('http://www.xxx.com', data=data)


    # 使用封装后的request
    @request(url='http://www.xxx.com')
    def get(value):
        data = {'key': value}
        return {'data': data}

之所以这么做,是因为这样可以更突显出api,更容易参数化,对session以及响应结果更好的处理


参数读取的大致流程如下:

.. image:: /_static/flow.png
  :width: 600 px

使用POST方法，传参方式为表单格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import request

    @request(url='http://httpbin.org/post', method='post')
    def post(self, key1='value1'):
        """
        post method
        """
        data = {
            'key1': key1
        }
        return dict(data=data)

    # 使用
    response = post('test').to_json()     # 解析json字符,输出为字典
    response = post('test').json          # 解析json字符,输出为字典
    response = post('test').to_content()  # 输出为字符串
    response = post('test').content       # 输出为字符串
    response = post('test').get_cookie()  # 输出cookie对象
    response = post('test').cookie        # 输出cookie对象

    # 结果取值, 假设此处response = {'a': 1, 'b': { 'c': [1, 2, 3, 4]}}
    response = post('13111111111', '123abc').json

    print response.b.c   # 通过点号取值,结果为[1, 2, 3, 4]

    print response('$.a') # 通过object path取值,结果为1

    for i in response('$..c[@>3]'): # 通过object path取值,结果为选中c字典里大于3的元素
        print i


使用POST方法，传参方式为JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import request

    @request(url='http://httpbin.org/post', method='post')
    def post(self, key1='value1'):
        """
        post method
        """
        data = {
            'key1': key1
        }
        return dict(json=data)


GET,URL传参
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import request

    @request(url='http://httpbin.org//get')
    def get(self, key1='value1', key2=None):
        """
        get method
        """
        if key2 is None:
            key2 = ['value2', 'value3']

        params = {
            'key1': key1,
            'key2': key2
        }
        return dict(params=params)


使用类的方式组织用接口
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用同一session,指定base_url

::

    from pithy import request

    class PithyAPP(object):

        def __init__(self):
            self.base_url = 'http://httpbin.org

        @request(url='/get')
        def get(self, key1='value1', key2=None):
            """
            get method
            """
            if key2 is None:
                key2 = ['value2', 'value3']

            params = {
                'key1': key1,
                'key2': key2
            }
            return dict(params=params)

        @request(url='post', method='post')
        def post(self, key1='value1'):
            """
            post method
            """
            data = {
                'key1': key1
            }
            return dict(data=data)

        @request(url='post', method='post')
        def json(self, key1='value1'):
            """
            post method
            """
            data = {
                'key1': key1
            }
            return dict(json=data)
        
        @request(url='login', method='post')
        def _login(username, password):
            """
            登录api
            注: 该方法只是示例,并不能运行,请结合自己的项目使用
            """
            data = {
                'username': username,
                'password': password
            }
            return dict(data=data)
        
        def login(username, password):
            """
            登录方法
            注: 该方法只是示例,并不能运行,请结合自己的项目使用
            """
            req = self._login(username, password)
            cookies = res.cookies  # 响应cookies
            headers = res.headers  # 响应headers
            self.session.headers.update(xxx=headers.get('xxx')) # 设置session里的headers,设置之后,所有的请求均会带上
            self.session.cookies.set('xxx', cookies.get('xxx')) # 设置session里的cookies,设置之后,所有的请求均会带上

    # 使用，此处两个接口使用同一request session请求
    app = PithyAPP()
    app.get('value1').to_json()
    app.post('value1).to_json()
