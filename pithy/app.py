#!/usr/bin/python
# coding=utf-8
"""
定义PO模式页面基类APP
"""

from appium.webdriver import Remote, WebElement
from appium.webdriver.common.mobileby import MobileBy as By
from .utils import fn_timer
import logging
import time


class MyList(list):
    """
    自定义LIST类型,以区别于其它LIST
    """
    pass


class _APPMetaclass(type):
    """
    页面类元类, 收集elements到_elements_字典
    """
    def __new__(mcs, name, bases, attrs):
        if name == 'APP':
            return type.__new__(mcs, name, bases, attrs)

        elements = dict()
        LOGGER = logging.getLogger(name)
        LOGGER.info(u'页面:%s' % name)
        for k, v in attrs.iteritems():
            if isinstance(v, MyList):
                LOGGER.info(u'      发现页面元素: %s ==> %s' % (k, v))
                elements[k] = v
        LOGGER.info('\n\n')

        for k in elements.iterkeys():
            attrs.pop(k)
        attrs['__page__'] = name
        attrs['__elements__'] = elements
        return type.__new__(mcs, name, bases, attrs)


class APP(object):
    """
    APP页面基类
    """
    __metaclass__ = _APPMetaclass
    driver_share = {}
    driver = None
    command_executor = None
    desired_capabilities = None

    def __init__(self):
        self.LOGGER = logging.getLogger(self.__class__.__name__)
        if not self.driver_share.get('driver'):
            self.driver = Remote(self.command_executor, desired_capabilities=self.desired_capabilities)
            self.driver_share['driver'] = self.driver
        else:
            self.driver = self.driver_share['driver']  # type: Remote

    @classmethod
    def init(cls, command_executor=None, desired_capabilities=None):
        if command_executor:
            cls.command_executor = command_executor
        if desired_capabilities:
            cls.desired_capabilities = desired_capabilities

    def __getattr__(self, item):
        try:
            element = self.__elements__[item]
        except IndexError:
            raise ValueError(u'没找到要查找的变量')

        time.sleep(0.4)
        total_time, element_object = self.__find_element(element)
        self.LOGGER.info(u'查找%s元素共用时: %s秒' % (item, total_time))
        return element_object

    @fn_timer
    def __find_element(self, element):
        if len(element) == 2:
            return self.driver.find_element(*element)
        elif len(element) == 3 and element[-1] == 'elements':
            return self.driver.find_elements(*element[:2])
        else:
            raise TypeError(u'Element(s)不正确')

    def quit(self):
        try:
            self.driver.quit()
            self.driver_share['driver'] = None
        except:
            pass


class Element(object):
    """
    封装element元素
    """

    def __new__(cls, *args):
        """
        :rtype: WebElement
        """
        args_copy = MyList(args)
        return args_copy


class Elements(object):
    """
    封装elements元素
    """

    def __new__(cls, *args):
        """
        :rtype: list of WebElement
        """
        args_copy = MyList(args)
        args_copy.append('elements')
        return args_copy
