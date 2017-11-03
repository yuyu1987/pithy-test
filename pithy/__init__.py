#!/usr/bin/python
# coding=utf-8
import logging
from .api import request, make_session
# from .thrift_client import thrift_client
# from .db import DB as db
from .human_time import HumanDateTime
from .json_processor import JSONProcessor
from .cfg import Config
from .utils import pretty_print

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)
get_config = config_manager = Config
