#!/usr/bin/python
# coding=utf-8
from pithy import request
import unittest


class DemoAPP(object):

    def __init__(self):
        self.base_url = 'http://httpbin.org/'

    @request(url='get')
    def get(self, value):
        params = {
            'key': value
        }
        return dict(params=params)


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = DemoAPP()

    def test_get(self):
        res = self.app.get(123).json
        assert res.args.key == '123'
