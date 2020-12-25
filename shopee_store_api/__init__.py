# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : shopee_sotre_api
# @Author  : lin
# @File    : __init__.py
"""
describe:

    api模块,向第三方平台(Shopee)通过api获取数据资源

"""


import os
import sys
import requests
from requests import utils
import logging
import json
import traceback

api_log_name = "api"


# api日志
def api_logger(api_path, api_name, msg, response: requests.Response = None, level=logging.INFO):

    log_data = {
        "api_path": api_path,
        "api_name": api_name,
        "module": "shopee_sotre_api",
        "request": {},
        "response": {},
        "msg": msg
    }
    if response is not None:
        log_data['response']['url'] = response.url
        log_data['response']['status'] = response.status_code
        log_data['response']['headers'] = dict(response.headers)
        log_data['response']['cookie'] = requests.utils.dict_from_cookiejar(response.cookies)
        log_data['response']['time'] = f"{response.elapsed.microseconds} ms"
        log_data['response']['text'] = response.text
        log_data['request']['url'] = response.request.url
        log_data['request']['headers'] = dict(response.request.headers)
        log_data['request']['method'] = response.request.method
        log_data['request']['body'] = response.request.body

    log_data = json.dumps(log_data)

    if level == logging.DEBUG:
        get_logger(api_log_name).debug(log_data)
    elif level == logging.INFO:
        get_logger(api_log_name).info(log_data)
    elif level == logging.ERROR:
        get_logger(api_log_name).error(log_data)
    elif level == logging.WARNING:
        get_logger(api_log_name).warning(log_data)


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.50 Safari/537.36"


# shopee 各个站点websocket地址
wss_url = {
    "ph": "wss://chat-ws.shopee.com.ph/socket.io/?EIO=3&transport=websocket",
    "sg": "wss://chat-ws.shopee.com.sg/socket.io/?EIO=3&transport=websocket",
    "vn": "wss://chat-ws.shopee.com.vn/socket.io/?EIO=3&transport=websocket",
    "th": "wss://chat-ws.shopee.com.th/socket.io/?EIO=3&transport=websocket",
    "id": "wss://chat-ws.shopee.com.id/socket.io/?EIO=3&transport=websocket",
    "my": "wss://chat-ws.shopee.com.my/socket.io/?EIO=3&transport=websocket",
    "br": "wss://chat-ws.shopee.com.br/socket.io/?EIO=3&transport=websocket"
}


# shopee 各个站点api地址
api_url = {
    'ph': 'https://seller.ph.shopee.cn',
    'sg': 'https://seller.sg.shopee.cn',
    'vn': 'https://seller.vn.shopee.cn',
    'th': 'https://seller.th.shopee.cn',
    'id': 'https://seller.id.shopee.cn',
    'my': 'https://seller.my.shopee.cn',
    'br': 'https://seller.br.shopee.cn',
}


SUCCESS_CODE = 200

time_out = 10

from .api_user import login
from .api_order import get_simple_order_ids, get_compact_order_list_by_order_ids
from .api_chat import messages, chat_login
