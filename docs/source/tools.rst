工具集
======================================

--------------------------------------

配置管理
--------------------------------------
读取项目根目录下，或者当前目录下的配置文件，默认文件名为 ``cfg.yaml`` ，可传入 ``file_name`` 改变，目前支持解析的配置文件类型有 ``.ini`` 、``.yaml`` 、``.cfg`` 、``.conf``

yaml解析
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

例如cfg.yaml配置文件内容如下::

    db:
        pithy_db:
            host: 127.0.0.1
            port: 3306
            username: user
            password: 111111

使用方法如下::

    from pithy import config_manager

    config = config_manager()
    print(config.db)
    print(config.db.pithy_db)


ini解析
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

例如cfg.ini配置文件内容如下::

    [pithy_db]

    host = 127.0.0.1
    port = 5432
    username = postgres
    password = postgres


使用方法如下::

    from pithy import config_manager

    config = config_manager(file_name='cfg.ini')
    print(config.db.pithy_db)

conf和cfg格式与ini使用方法一致


日期处理
--------------------------------------

取当前时间
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import HumanDateTime
    print(HumanDateTime())


解析时间戳
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
解析任何有效的时间戳::

    from pithy import HumanDateTime

    # 解析时间戳
    print(repr(HumanDateTime(1490842267)))
    print(HumanDateTime(1490842267000))
    print(HumanDateTime(1490842267.11111))
    print(HumanDateTime(1490842267111.01))

解析字符串格式日期
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
解析常见字符串格式日期或时间::

    from pithy import HumanDateTime

    # 解析字符串格式日期
    print(HumanDateTime('2017-02-02'))
    print(HumanDateTime('Thu Mar 30 14:21:20 2017'))
    print(HumanDateTime(time.ctime()))
    print(HumanDateTime('2017-3-3'))
    print(HumanDateTime('3/3/2016'))
    print(HumanDateTime('2017-02-02 00:00:00'))

解析datetime或date类型时间
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import HumanDateTime

    # 解析datetime或date类型时间
    print(HumanDateTime(datetime(year=2018, month=11, day=30, hour=11)))
    print(HumanDateTime(date(year=2018, month=11, day=30)))


增加减少时间
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import HumanDateTime
    # 增加减少时间
    print(HumanDateTime('2017-02-02').add_day(1))
    print(HumanDateTime('2017-02-02').sub_day(1))
    print(HumanDateTime('2017-02-02').add_hour(1))
    print(HumanDateTime('2017-02-02').sub_hour(1))
    print(HumanDateTime('2017-02-02').add(days=1, hours=1, weeks=1, minutes=1, seconds=6))
    print(HumanDateTime('2017-02-02').sub(days=1, hours=1, weeks=1, minutes=1, seconds=6))


转换为时间戳
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
把任何格式的时间类型转换为时间戳::
    
    from pithy import HumanDateTime
    
    # 转换为时间戳
    print(HumanDateTime(1490842267.11111).timestamp_second)
    print(HumanDateTime(1490842267.11111).timestamp_microsecond)
    print(HumanDateTime('2017-02-02 12:12:12.1111').add_day(1).timestamp_microsecond)
    print(HumanDateTime('2017-02-02 12:12:12 1111').add_day(1).timestamp_microsecond)


比较大小
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
比较任何两个日期类型数据的大小::

    from pithy import HumanDateTime

    # 比较大小
    print(HumanDateTime('2017-02-02 12:12:12 1111') < HumanDateTime('2017-02-02 12:12:11 1111'))
    print(HumanDateTime('2017-02-02 12:12:12 1111') < HumanDateTime('2017-02-02 12:13:11 1111'))
    print(HumanDateTime('2017-02-02 12:12:12 1111') < '2017-02-02 12:11:11')
    print(HumanDateTime('2017-02-02 12:12:12 1111') < '2017-02-02 12:13:11 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') == '2017-02-02 12:13:11 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') == '2017-02-02 12:13:12 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') <= '2017-02-02 12:13:11 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') >= '2017-02-02 12:13:11 1111')
    print(HumanDateTime('2017-02-02 12:12:12 1111') != time.time())
    print(HumanDateTime('2017-02-02 12:12:12 1111') <= time.time())
    print(HumanDateTime('2017-02-02 12:12:12 1111') >= time.time())

    # 约等于或者接近
    print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:11 1111'))
    print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:10 1111'))
    print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:10 1111', offset=2))
    print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:14 1111', offset=2))


调用datetime的方法和属性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import HumanDateTime

    # 调用datetime的方法和属性
    print(HumanDateTime('2017-02-02 12:12:12 1111').day)
    print(HumanDateTime('2017-02-02 12:12:12 1111').year)
    print(HumanDateTime('2017-02-02 12:12:12 1111').second)
    print(HumanDateTime('2017-02-02 12:12:12 1111').date())


操作复杂JSON或字典
--------------------------------------
优化JSON字符串和字典的取值方式，输入为python字典或者json字符串，可以通过点号或者 `object path <http://objectpath.org/reference.html>`_ 对结果取值


操作JSON的KEY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import JSONProcessor
    dict_data = {'a': 1, 'b': {'a': [1, 2, 3, 4]}}
    json_data = json.dumps(dict_data)
    result = JSONProcessor(json_data)
    print result.a     # 结果：1
    print result.b.a   # 结果：[1, 2, 3, 4]


操作字典的KEY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pithy import JSONProcessor
    dict_data = {'a': 1, 'b': {'a': [1, 2, 3, 4]}}
    result = JSONProcessor(dict_data)
    print result.a     # 1
    print result.b.a   # [1, 2, 3, 4]

object path取值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
这里使用的object path的取值方式,详细语法见:http://objectpath.org/reference.html

::

    from pithy import JSONProcessor
    raw_dict = {
        'key1':{
            'key2':{
                'key3': [1, 2, 3, 4, 5, 6, 7, 8]
            }
        }
    }

    jp = JSONProcessor(raw_dict)
    for i in jp('$..key3[@>3]'):
        print i

结果是::
     
     4 
     5 
     6 
     7 
     8


其它用法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    dict_1 = {'a': 'a'}
    json_1 = '{"b": "b"}'
    jp = JSONProcessor(dict_1, json_1, c='c')
    print(jp)

输出为::

    {
        "a": "a",
        "b": "b",
        "c": "c"
    }

美化JSON打印
--------------------------------------
该函数是格式化打印 ``JSON`` 或 ``字典`` ，并对JSON中的unicode或utf-8字符进行转换

使用方法如下::

    from pithy import pretty_print
    d = {
        "args": {
            "name": "鱼鱼"
        },
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "Connection": "close",
            "Cookie": "_gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1",
            "Dnt": "1",
            "Host": "httpbin.org",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
        "origin": "157.119.234.165",
        "url": "http://httpbin.org/get"
    }
    print(d)
    print('\n\n)
    pretty_print(d) # 该处也可以传入JSON字符串

输出结果为::

        {'origin': '157.119.234.165', 'headers': {'Dnt': '1', 'Connection': 'close', 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4', 'Accept-Encoding': 'gzip, deflate, sdch', 'Cookie': '_gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'Host': 'httpbin.org', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Upgrade-Insecure-Requests': '1'}, 'args': {'name': '\xe9\xb1\xbc\xe9\xb1\xbc'}, 'url': 'http://httpbin.org/get'}
        

        {
            "args": {
                "name": "鱼鱼"
            },
            "headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
                "Connection": "close",
                "Cookie": "_gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1",
                "Dnt": "1",
                "Host": "httpbin.org",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
            "origin": "157.119.234.165",
            "url": "http://httpbin.org/get"
        }