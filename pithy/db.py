#!/usr/bin/python
# coding=utf-8
import sys
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class _DB(object):
    def __init__(self, database_info, name):
        self.database_info = database_info
        self.database_name = name
        self.base = None
        self.session = None

    def load(self):
        self._init_db()
        sys.modules[self.database_name] = self
        return self

    def _init_db(self):
        self.base = automap_base()
        engine = create_engine(self.database_info)
        self.base.prepare(engine, reflect=True)
        self.session = Session(engine)

    def __getattr__(self, table_name):
        try:
            table_object = getattr(self.base.classes, table_name)
        except AttributeError:
            raise Exception(u'没找到:{table_name}'.format(table_name=table_name))
        return table_object


class DB(object):
    """
    example:
    DB("mysql://user:password@host:port/database?charset=utf8", 'pithy_db')
    from pithy_db import o_order, session
    query_result = session.query(o_order).all()
    """

    db_pool = {}

    def __new__(cls, database_info, name):
        if name in cls.db_pool:
            return cls.db_pool[name]
        else:
            db_module = _DB(database_info, name).load()
            cls.db_pool[name] = db_module
            return db_module
