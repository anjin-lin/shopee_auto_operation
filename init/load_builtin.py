# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : init
# @Author  : lin
# @File    : load_builtin.py
"""
describe:

    加载运行脚本的全局内置模块或函数

"""

from . import BaseLoad, builtins_container
import builtins


class LoadBuiltin(BaseLoad):

    def load(self):

        for builtin in builtins_container:
            setattr(builtins, builtin, builtins_container[builtin])

