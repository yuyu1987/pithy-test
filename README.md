## 一、安装&更新
```sh
# 安装
pip install pithy-test

# 更新
pip install -U pithy-test
```

## 二、生成接口测试项目

```shell
(pyenv)$  ~ pithy-cli init
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
```


## 三、接口测试

### 3.1、HTTP接口
* 在函数中定义按需定义headers, body, params(url参数)

#### 3.1.1、使用POST方法

```python
from pithy import request

@request(url='http://xxxx/login', method='post')
def login(phone=None, password=None):
    """
    登录
    """
    headers = {'xx': xx, 'xx': xx}
    body = {
        'phone': phone,
        'password': password
    }

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
```

#### 3.1.2、使用GET方法,数据传输方式为json方式


```python
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

```


#### 3.1.3、使用POST方法,数据传输方式为form方式


```python
from pithy import request

@request(url='http://xxxx/login', method='post', data_type='form')
def login(phone=None, password=None):
    """
    登录
    """
    headers = {'xx': xx, 'xx': xx}
    body = {
        'phone': phone,
        'password': password
    }

```

#### 3.1.4、使用类的方式组织用接口,使用同一session,指定base_url


```python
from pithy import request

class PithyApp(object):
    """
    PithyApp 相关接口
    """
    def __init__(self):
        self.session = None  # 定义session，方便后面操作, 同时也可以不定义self.session,会自动创建
        self.base_url = 'http://xxx.com'  # 指定base_url,也可以不指定

    @request(url='login', method='form')
    def _login(self, phone=None, password=None):
        """
        登录接口
        """
        headers = {'xx': xx, 'xx': xx}
        body = {
            'phone': phone,
            'password': password
        }
    
    def login(self, phone=None, password=None):
        """
        登录
        """
        login_response = self._login('13111111111', '111111').to_json()
        self.session.cookies.set('session', login_response.data.session)
    
    @request(url='pithy-webapi/get_info')
    def get_info(self):
        """
        获取信息
        """
        pass


# 使用，此处两个接口使用同一request session请求
pithy = Pithy()
pithy.login('13111111111', '123abc').json
pithy.get_info().json


```

#### 3.1.5、不使用类组织接口，使用指定的session


```python
from pithy import request, make_session

@request(url=config.BASE_URL + '/pithy-webapi/login', method='form')
def login(phone=None, password=None, session=None):
    """
    登录
    """
    headers = {'xx': xx, 'xx': xx}
    body = {
        'phone': phone,
        'password': password
    }

# 调用
session = make_session()
response = login('13111111111', '123abc', session=session).json

```

### 3.2、thrift接口
thrift接口测试对thriftpy进行了简单封装,不需要再去构造struct,直接使用字典的形式就可以调用
#### 使用方法:
* 定义一个类,类名和thrift service名要一致,在类上方使用thrift_client装饰器,然后在初始化方法中定义host和port以及指定thrift文件
* 定义要调用的thrift方法,在类中定义,名字与thrift名字要一致
* 在thrift方法中传参,可以在方法体中传,也可以在参数列表中定义,变量与应与thrift中定义的一致,struct结构应转化成字典格式

#### 示例代码如下:
该示例代码为调用Pithy服务中的一个充值方法

```python
import hashlib
import uuid
from pithy import thrift_client

@thrift_client
class PithyService(object):
    def __init__(self):
        self.host = 'xxx.xxx.xxx.xxx'
        self.port = xxxx
        self.thrift_file = 'pithy.thrift'

    def charge(self, _id, amount):
        """
        thrift方法
        """
        remark = 'test'
        base_request = {
            'id': _id,
            'amount': amount,
            'sign': '111111111111'
        }

print(PithyService().charge(1111, 100 * 1000).base_response.remark)

```

执行结果如下:

```shell

********************************************

1、请求方法:
pithy_thrift.PithyService.charge

2、请求参数:
{'remark': 'test', 'base_request': BaseRequest(id=1111, sign='111111111111', amount=10000}

3、响应结果:
AccountChargeResponse(charge_sn=u'xxxxxx', base_response=BaseResponse(remark=u'\u6210\u529f'))


成功
```


## 四、数据库相关
这里使用sqlalchemy orm,使用方法如下:

```python
from pithy import db
pithy_db = db("mysql://user:password@host:port/database?charset=utf8", 'pithy_db')

# 使用从模块导入方式
from pithy_db import order, session
query_result = session.query(order).all()

# 不使用从模块导入的方式
order = pithy_db.order
session = pithy_db.session
session.query(order).all()
```

## 五、工具类
### 5.1、操作日期函数 
```python
from pithy import HumanDateTime

# 解析时间戳
print repr(HumanDateTime(1490842267))
print HumanDateTime(1490842267000)
print HumanDateTime(1490842267.11111)
print HumanDateTime(1490842267111.01)

# 解析字符串格式日期
print HumanDateTime('2017-02-02')
print HumanDateTime('Thu Mar 30 14:21:20 2017')
print HumanDateTime(time.ctime())
print HumanDateTime('2017-3-3')
print HumanDateTime('3/3/2016')
print HumanDateTime('2017-02-02 00:00:00')

# 解析datetime或date类型时间
print HumanDateTime(datetime(year=2018, month=11, day=30, hour=11))
print HumanDateTime(date(year=2018, month=11, day=30))

# 增加减少时间
print HumanDateTime('2017-02-02').add_day(1)
print HumanDateTime('2017-02-02').sub_day(1)
print HumanDateTime('2017-02-02').add_hour(1)
print HumanDateTime('2017-02-02').sub_hour(1)
print HumanDateTime('2017-02-02').add(days=1, hours=1, weeks=1, minutes=1, seconds=6)
print HumanDateTime('2017-02-02').sub(days=1, hours=1, weeks=1, minutes=1, seconds=6)

# 转换为时间戳
print HumanDateTime(1490842267.11111).timestamp_second
print HumanDateTime(1490842267.11111).timestamp_microsecond
print HumanDateTime('2017-02-02 12:12:12.1111').add_day(1).timestamp_microsecond
print HumanDateTime('2017-02-02 12:12:12 1111').add_day(1).timestamp_microsecond

# 比较大小
print HumanDateTime('2017-02-02 12:12:12 1111') < HumanDateTime('2017-02-02 12:12:11 1111')
print HumanDateTime('2017-02-02 12:12:12 1111') < HumanDateTime('2017-02-02 12:13:11 1111')
print HumanDateTime('2017-02-02 12:12:12 1111') < '2017-02-02 12:11:11'
print HumanDateTime('2017-02-02 12:12:12 1111') < '2017-02-02 12:13:11 1111'
print HumanDateTime('2017-02-02 12:12:12 1111') == '2017-02-02 12:13:11 1111'
print HumanDateTime('2017-02-02 12:12:12 1111') == '2017-02-02 12:13:12 1111'
print HumanDateTime('2017-02-02 12:12:12 1111') <= '2017-02-02 12:13:11 1111'
print HumanDateTime('2017-02-02 12:12:12 1111') >= '2017-02-02 12:13:11 1111'
print HumanDateTime('2017-02-02 12:12:12 1111') != time.time()
print HumanDateTime('2017-02-02 12:12:12 1111') <= time.time()
print HumanDateTime('2017-02-02 12:12:12 1111') >= time.time()

# 约等于或者接近
print HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:11 1111')
print HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:10 1111')
print HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:10 1111', offset=2)
print HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:14 1111', offset=2)

# 调用datetime的方法和属性
print HumanDateTime('2017-02-02 12:12:12 1111').day
print HumanDateTime('2017-02-02 12:12:12 1111').year
print HumanDateTime('2017-02-02 12:12:12 1111').second
print HumanDateTime('2017-02-02 12:12:12 1111').date()
```

### 5.2、操作复杂JSON或字典
优化JSON字符串和字典的取值方式

```python
# 1、操作JSON的KEY
from pithy import JSONProcessor
dict_data = {'a': 1, 'b': {'a': [1, 2, 3, 4]}}
json_data = json.dumps(dict_data)
result = JSONProcessor(json_data)
print result.a     # 结果：1
print result.b.a   # 结果：[1, 2, 3, 4]

# 这里使用的object path的取值方式,详细语法见:http://objectpath.org/reference.html
for i in result('$..a[@>3]'):  # 结果： 4
    print i

# 2、操作字典的KEY
dict_data = {'a': 1, 'b': {'a': [1, 2, 3, 4]}}
result = JSONProcessor(dict_data)
print result.a     # 1
print result.b.a   # [1, 2, 3, 4]
```