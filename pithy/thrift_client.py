#!/usr/bin/python
# coding=utf-8
import os
import sys
import thriftpy
from thriftpy.rpc import make_client

LOG_FORMAT = u'''
********************************************

1、请求方法:
{thrift_module_name}.{service_name}.{function_name}

2、请求参数:
{thrift_kwargs}

3、响应结果:
{response}

'''


def thrift_service_wrapper(func):
    def get_params(func, *args, **kwargs):
        get_params.locals = {}

        def tracer(frame, event, arg):
            if event == 'return':
                get_params.locals = frame.f_locals.copy()

        sys.setprofile(tracer)
        func(*args, **kwargs)
        params = get_params.locals
        get_params.locals = {}
        return params

    def assemble_struct(struct_obj, dict_obj):
        for value in struct_obj.thrift_spec.values():
            if isinstance(value[2], thriftpy.thrift.TPayloadMeta):
                dict_obj[value[1]] = assemble_struct(value[2], dict_obj[value[1]])
            elif isinstance(value[2], (tuple, list)):
                if isinstance(value[2][1], thriftpy.thrift.TPayloadMeta):
                    dict_obj[value[1]] = [assemble_struct(value[2][1], d) for d in dict_obj[value[1]]]
        return struct_obj(**dict_obj)

    def assemble_kwargs(function_args_dict, params_dict):
        result = {}
        for value in function_args_dict.thrift_spec.values():
            if isinstance(value[2], thriftpy.thrift.TPayloadMeta):
                result[value[1]] = assemble_struct(value[2], params_dict[value[1]])
            elif isinstance(value[2], (tuple, list)):
                if isinstance(value[2][1], thriftpy.thrift.TPayloadMeta):
                    result[value[1]] = [assemble_struct(value[2][1], d) for d in params_dict[value[1]]]
            else:
                result[value[1]] = params_dict[value[1]]

        return result

    def function_wrapper(*args, **kwargs):
        function_name = func.__name__
        service_class_ins = func.im_self
        service_name = service_class_ins.__class__.__name__
        thrift_module = service_class_ins.thrift_module
        thrift_service_ins = getattr(thrift_module, service_name)
        function_args_dict = getattr(thrift_service_ins, function_name + '_args')
        user_params_dict = get_params(func, *args, **kwargs)
        thrift_kwargs = assemble_kwargs(function_args_dict, user_params_dict)
        client = make_client(thrift_service_ins, host=service_class_ins.host, port=int(service_class_ins.port))

        try:
            response = getattr(client, function_name)(**thrift_kwargs)
        finally:
            client.close()

        print(LOG_FORMAT.format(thrift_module_name=thrift_module.__name__,
                                service_name=service_name,
                                function_name=function_name,
                                thrift_kwargs=thrift_kwargs,
                                response=response))
        return response
    return function_wrapper


def thrift_client(cls):
    def cls_wrapper(*args, **kwargs):
        def __getattribute__(self, item):
            thrift_module = object.__getattribute__(self, 'thrift_module')
            service_name = object.__getattribute__(self, '__class__').__name__
            thrift_services = getattr(thrift_module, service_name)
            thrift_services_list = thrift_services.thrift_services
            if item in thrift_services_list:
                return thrift_service_wrapper(object.__getattribute__(self, item))
            else:
                return object.__getattribute__(self, item)

        service_client_instance = cls(*args, **kwargs)
        thrift_file = service_client_instance.thrift_file
        thrift_module_name = os.path.splitext(os.path.basename(thrift_file))[0] + '_thrift'
        thrift_module = thriftpy.load(thrift_file, module_name=thrift_module_name)
        setattr(cls, 'thrift_module', thrift_module)
        setattr(cls, '__getattribute__', __getattribute__)
        return service_client_instance

    return cls_wrapper
