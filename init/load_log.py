# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : init
# @Author  : lin
# @File    : load_log.py
"""
describe:

    加载日志

"""


from . import BaseLoad, get_config, builtins_container, os, sys
import logging
from logging import handlers, config


class LoadLog(BaseLoad):

    def load(self):

        log_path = os.getenv("LOG_PATH", "./logs")

        # 判断日志目录是否存在
        if not os.path.exists(log_path) and not os.path.isdir(log_path):
            os.mkdir(log_path)

        # 日志配置信息
        log_info = get_config(config_name="", config_attr="log_info")

        logging.config.dictConfig(log_info)

        builtins_container["get_logger"] = self.get_logger

        sys.excepthook = self.handle_exception

    @staticmethod
    def get_logger(logger_name: str = ""):

        if not logger_name:
            logger_name = "default"

        logger = logging.getLogger(logger_name)

        return logger

    # 全部异常写入日志
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # 将异常错误写入日志
        self.get_logger("importance").error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))





