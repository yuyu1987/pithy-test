#!/usr/bin/python
# coding=utf-8
import yaml
import os
import sys


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

    print config['pithy_db]['host']  # 取值
    ...

    """
    config_object_instance = {}

    def __new__(cls, config_file_name='cfg.yaml', *args, **kwargs):
        if config_file_name not in cls.config_object_instance.keys():
            config_file_path = config_file_name
            if not os.path.exists(config_file_name):
                config_file_path0 = os.path.join(sys.path[0], config_file_name)
                config_file_path1 = os.path.join(sys.path[1], config_file_name)
                if os.path.exists(config_file_path0):
                    config_file_path = config_file_path0
                elif os.path.exists(config_file_path1):
                    config_file_path = config_file_path1
                else:
                    raise OSError(u'未找到指定的配置文件,请在项目根目录下放置cfg.yaml 或 指定路径')

            cls.config_object_instance[config_file_name] = yaml.load(open(config_file_path))

        return cls.config_object_instance[config_file_name]

    def __getitem__(self, item):
        return self[item]
