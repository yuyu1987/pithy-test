快速开始
======================================

--------------------------------------

生成测试项目
--------------------------------------

::

    >>> pithy-cli init
    请选择项目类型,输入api或者app: api
    请输入项目名称,如pithy-api-test: pithy-api-test
    开始创建pithy-api-test项目
    开始渲染...
    开始渲染 api/.gitignore.jinja
    开始渲染 api/apis/__init__.py.jinja
    开始渲染 api/apis/pithy_api.py.jinja
    开始渲染 api/cfg.yaml.jinja
    开始渲染 api/db/__init__.py.jinja
    开始渲染 api/db/pithy_db.py.jinja
    开始渲染 api/README.MD.jinja
    开始渲染 api/requirements.txt.jinja
    开始渲染 api/test_suites/__init__.py.jinja
    开始渲染 api/test_suites/test_login.py.jinja
    开始渲染 api/utils/__init__.py.jinja
    生成成功,请使用编辑器打开该项目

.. attention::
  app还未开发，暂时还不能生成


HTTP API测试
--------------------------------------

**使用POST方法，传参方式为表单格式**::

    from pithy import request

    @request(url='http://xxxx/login', method='post')
    def login(phone=None, password=None):
        """
        登录
        """
        headers = {'xx': xx, 'xx': xx}
        data = {
            'phone': phone,
            'password': password
        }
        return dict(headers=headers, data=data)

    # 使用
    response = login('13111111111', '123abc').to_json()     # 解析json字符,输出为字典
    response = login('13111111111', '123abc').json          # 解析json字符,输出为字典
    response = login('13111111111', '123abc').to_content()  # 输出为字符串
    response = login('13111111111', '123abc').content       # 输出为字符串
    response = login('13111111111', '123abc').get_cookie()  # 输出cookie对象
    response = login('13111111111', '123abc').cookie        # 输出cookie对象

    # 结果取值, 假设此处response = {'a': 1, 'b': { 'c': [1, 2, 3, 4]}}
    response = login('13111111111', '123abc').json

    print response.b.c   # 通过点号取值,结果为[1, 2, 3, 4]

    print response('$.a') # 通过object path取值,结果为1

    for i in response('$..c[@>3]'): # 通过object path取值,结果为选中c字典里大于3的元素
        print i


**使用POST方法，传参方式为JSON**::

    from pithy import request

    @request(url='http://xxxx/login', method='post')
    def login(phone=None, password=None):
        """
        登录
        """
        headers = {'xx': xx, 'xx': xx}
        data = {
            'phone': phone,
            'password': password
        }
        return dict(headers=headers, json=data)


**GET,URL传参**::

    from pithy import request

    @request(url='http://xxxx/login')
    def login(phone=None, password=None):
        """
        登录
        """
        headers = {'xx': xx, 'xx': xx}
        params = {
            'phone': phone,
            'password': password
        }
        return dict(headers=headers, params=params)
