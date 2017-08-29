# coding=utf-8

import unittest
from pithy import Config


class TestConfig(unittest.TestCase):

    def test_json_config(self):
        cfg = Config('cfg.json')
        assert cfg['a'] == 1
        assert cfg['b'] == [2, 3]
        assert cfg['c'] == {'d': 1}
