# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : config
# @Author  : lin
# @File    : __init__.py
"""
describe:

    配置模块,应用执行时所需要的配置,
    基础配置: Config类中的一些配置属性
    redis配置, 日志配置, 数据库的配置,
    需要加载其他配置,在这个模块中新建一个配置的py文件
    在这个py文件中引入当前__init__中的配置基类BaseConfig
    继承实现这个基类,get_config方法会自动通过config_name属性
    来加载你的配置;
    注：get_config已经被加载到了全局内置函数中,在需要获取配置
    的代码中直接执行config方法.

"""


import os
from abc import ABCMeta, abstractmethod

# 配置缓存容器(其实就是一个字典)
Configs = {}


# 配置项基类
class BaseConfig(metaclass=ABCMeta):

    @property
    @abstractmethod
    def config_name(self) -> str:
        return str()


# 获取配置(这个会被加载到内置函数里面;函数名：config)
def get_config(config_name: str = "", config_attr: str = ""):

    # 指定配置项名称为空则默认走默认配置
    if not config_name:
        config_name = "default"

    # 配置数据
    config_data = None

    # 先从配置缓存列表获取, 没有则从配置文件获取
    if config_name in Configs.keys():
        config_data = Configs[config_name]
    else:
        configs = BaseConfig.__subclasses__()
        for conf in configs:
            if config_name == conf.config_name:
                Configs[config_name] = conf()
                config_data = Configs[config_name]

    # 是否只获取配置数据里面的某个配置属性, 不是则返回整个配置数据
    if config_data is not None and config_attr is not None:
        return getattr(config_data, config_attr)
    else:
        return config_data


from .config import Config
