# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : init
# @Author  : lin
# @File    : load_env.py
"""
describe:

    加载运行脚本的环境变量

"""


from . import BaseLoad, os
from dotenv import load_dotenv, find_dotenv


class LoadEnv(BaseLoad):

    def load(self):
        dotenv_path = find_dotenv()

        if os.path.exists(dotenv_path):
            # override=True: 覆写已存在的变量
            load_dotenv(dotenv_path, override=True)


