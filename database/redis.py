# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : database
# @Author  : lin
# @File    : redis.py
"""
describe:

    redis数据配置

"""


import redis

# 从配置文件中获取redis连接信息
redis_conn_info = config(config_name="", config_attr="redis")

# redis连接池
r_pool = redis.ConnectionPool(host=redis_conn_info['host'], port=redis_conn_info['port'])


# 获取一个redis实例
def get_redis():

    # 创建一个Redis对象
    redis_obj = redis.Redis(connection_pool=r_pool, db=redis_conn_info['database'])

    return redis_obj
