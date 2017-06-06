#!/usr/bin/python
# coding=utf-8
import yaml
import os
import sys
from configobj import ConfigObj
from .json_processor import JSONProcessor


class Config(object):
    """
    读取yaml格式配置文件,并返回指定的环境配置
    注意:
      1、优先读取当前目录下, 第二顺序读取项目根目录下
      2、同一名称配置文件只加载一次,再次实例化不再加载
      3、默认返回beta环境配置,如果系统环境变量中有指定,则返回系统环境变量所指定的

    使用:
    from pithy import get_config
    config = get_config()  # 使用默认配置文件名cfg.yaml
    config = get_config('pithy.yaml')  # 使用自定义配置文件

    print config.pithy_db.host  # 取值
    ...

    """
    config_object_instance = {}

    def __new__(cls, file_name='cfg.yaml', *args, **kwargs):
        if file_name not in cls.config_object_instance.keys():
            config_file_path = file_name
            if not os.path.exists(file_name):
                config_file_path0 = os.path.join(sys.path[0], file_name)
                config_file_path1 = os.path.join(sys.path[1], file_name)
                if os.path.exists(config_file_path0):
                    config_file_path = config_file_path0
                elif os.path.exists(config_file_path1):
                    config_file_path = config_file_path1
                else:
                    raise OSError('can not find config file !')
            if file_name.endswith('.yaml'):
                cls.config_object_instance[file_name] = yaml.load(open(config_file_path))
            elif file_name.endswith(('.cfg', '.ini', '.conf')):
                cls.config_object_instance[file_name] = ConfigObj(config_file_path)
            else:
                raise ValueError('Unsupported configuration file type')

        return JSONProcessor(cls.config_object_instance[file_name])

    def __getitem__(self, item):
        return self[item]
