thrift接口
======================================
thrift接口测试对thriftpy进行了简单封装,不需要再去构造struct,直接使用字典的形式就可以调用

使用方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 定义一个类,类名和thrift service名要一致,在类上方使用thrift_client装饰器,然后在初始化方法中定义host和port以及指定thrift文件
- 定义要调用的thrift方法,在类中定义,名字与thrift名字要一致
- 在thrift方法中传参,可以在方法体中传,也可以在参数列表中定义,变量与应与thrift中定义的一致,struct结构应转化成字典格式

示例代码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
该示例代码为调用Pithy服务中的一个充值方法::

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

执行结果为::

    *******************************************

    1、请求方法:
    pithy_thrift.PithyService.charge

    2、请求参数:
    {'remark': 'test', 'base_request': BaseRequest(id=1111, sign='111111111111', amount=10000}

    3、响应结果:
    AccountChargeResponse(charge_sn=u'xxxxxx', base_response=BaseResponse(remark=u'\u6210\u529f'))


    成功

