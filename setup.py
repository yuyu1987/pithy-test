#!/usr/bin/python
# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="pithy-test",
    version="0.0.19",
    keywords=("interface", "automation", "testing", "pithy"),
    description="Simplify interface testing",
    long_description="Simplify interface testing",
    url="https://github.com/yuyu1987/pithy-test",
    author="coolfish",
    author_email="hgbaczt@gmail.com",
    packages=['pithy'],
    include_package_data=True,
    platforms="any",
    install_requires=['requests', 'records', 'objectpath', 'click',
                      'jinja2', 'pyyaml', 'configobj'],
    entry_points='''
    [console_scripts]
    pithy-cli=pithy.cli:cli
    '''
)
