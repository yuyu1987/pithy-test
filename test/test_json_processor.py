#!/usr/bin/python
# coding=utf-8
from pithy import JSONProcessor
import json
import unittest


class TestJSONProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.raw_dict = {
            'key1': 1,
            'key2': [1, 2, 3, 4],
            'key3': {
                'key31': 1,
                'key32': '我'
            }
        }

        cls.raw_json = json.dumps(cls.raw_dict)

    def test_1(self):
        jp = JSONProcessor(self.raw_dict)
        assert jp.key1 == 1
        assert jp.key3.key31 == 1
        assert jp.key3.key32 == '我'

        jp2 = JSONProcessor(self.raw_json)
        assert jp2.key1 == 1
        assert jp2.key3.key31 == 1
        assert jp2.key3.key32 == u'我'

    def test_2(self):
        jp = JSONProcessor(self.raw_dict, key4=4)
        assert jp.key4 == 4

        jp2 = JSONProcessor(self.raw_json, {'key4': 4})
        assert jp2.key4 == 4

    def test_3(self):
        jp = JSONProcessor(self.raw_dict)
        assert jp('$.key1') == 1

    def test_4(self):
        jp = JSONProcessor(self.raw_dict)
        print(str(jp))
        print(unicode(jp))
