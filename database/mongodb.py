# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 11:17
# @Module  : database
# @Author  : lin
# @File    : mongodb.py
"""
describe:

    mongodb数据配置

"""

import pymongo


# mongodb连接信息
mongo_conn_info = config(config_name="", config_attr="mongo")

if not mongo_conn_info['account']:
    mongo_client = pymongo.MongoClient(f"mongodb://{mongo_conn_info['host']}:{mongo_conn_info['port']}/")
else:
    mongo_client = pymongo.MongoClient(f"mongodb://{mongo_conn_info['account']}:{mongo_conn_info['password']}@{mongo_conn_info['host']}:{mongo_conn_info['port']}/")

mongo_database = mongo_client[mongo_conn_info['database']]


# 获取一个mongodb连接实例
def get_mongodb(collection_name: str):

    collection = mongo_database[collection_name]

    return collection
