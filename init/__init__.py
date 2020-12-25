# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : init
# @Author  : lin
# @File    : __init__.py
"""
describe:

    初始化模块,加载应用运行时所需的资源
    基础资源: 环境变量, 日志, 提供全局调用的内置模块;
    需要加载其他资源,在模块中新建一个加载资源的py文件
    在这个py文件中引入当前__init__中的加载基类BaseLoad
    继承实现这个基类,init方法会自动执行你的load方法
    来加载你的资源.

"""


import os
import sys
from abc import ABCMeta, abstractmethod
from config import get_config
import helper_functions

# 设置全局函数容器,在这个容器里面的资源将被LoadBuiltin类加载到全局,可以用引入直接调用
builtins_container = {
    "config": get_config,
    "helper": helper_functions,
}


# 加载资源基类(抽象类)
class BaseLoad(metaclass=ABCMeta):

    @abstractmethod
    def load(self):
        pass


# 初始化资源加载
def init():
    # 获取加载资源基类的所有子类
    loads = BaseLoad.__subclasses__()
    for load_cls in loads:
        ld = load_cls()  # 实例化加载类
        ld.load()  # 执行加载资源

    from scripts import ScriptApplication

    return ScriptApplication()


from .load_env import LoadEnv  # 加载环境变量
from .load_log import LoadLog  # 加载日志
from .load_builtin import LoadBuiltin   # 加载全局内置函数(如助手函数,不用引入模块包直接使用的函数)
