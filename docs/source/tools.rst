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

    # 这里使用的object path的取值方式,详细语法见:http://objectpath.org/reference.html
    for i in result('$..a[@>3]'):  # 结果： 4
        print i


操作字典的KEY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    dict_data = {'a': 1, 'b': {'a': [1, 2, 3, 4]}}
    result = JSONProcessor(dict_data)
    print result.a     # 1
    print result.b.a   # [1, 2, 3, 4]
