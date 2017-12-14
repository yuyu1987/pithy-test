# coding=utf-8
import time
import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By

UPLOAD_EXE_PATH = os.path.join(os.path.dirname(__file__), 'upload.exe')


def time_check(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        print(u'查找【%s】元素用时%.3f秒' % (args[1], t2 - t1))
        return res
    return wrapper


class BasePage(object):
    driver = None  # type:webdriver.Chrome

    def __new__(cls, *args, **kwargs):
        if not cls.driver:
            cls.driver = webdriver.Chrome()
        return object.__new__(cls, *args, **kwargs)

    def element(self, item):
        """
        :rtype: WebElement
        """
        try:
            value = self.locators[item]
        except:
            raise Exception(u'没有定义【%s】元素的定位方式，请检查locators' % item)
        return self.find_element(item, value)

    def elements(self, item):
        """
        :rtype: list of WebElement
        """
        try:
            value = self.locators[item]
        except:
            raise Exception(u'没有定义【%s】元素的定位方式，请检查locators' % item)
        return self.find_elements(item, value)

    @staticmethod
    def upload(file_path):
        os.system('{exe_path} {file_path}'.format(exe_path=UPLOAD_EXE_PATH, file_path=file_path))

    @time_check
    def find_element(self, item, value):
        try:
            return self.driver.find_element(*value)
        except:
            raise Exception(u'没有找到元素【%s】' % item)

    @time_check
    def find_elements(self, item, value):
        try:
            return self.driver.find_elements(*value)
        except:
            raise Exception(u'没有找到元素【%s】' % item)

    @classmethod
    def quit(cls):
        try:
            cls.driver.quit()
        except:
            pass
        finally:
            cls.driver = None
