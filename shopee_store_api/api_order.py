# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 10:38
# @Module  : shopee_sotre_api
# @Author  : lin
# @File    : api_order.py
"""
describe:

    订单资源api

"""


from . import api_url, SUCCESS_CODE, time_out, user_agent, requests, logging, api_logger, traceback


# 获取查询订单分词查询后的关联ID组(通过ID组可以查询到对于的订单信息)
def get_simple_order_ids(data: dict, country, cookies: dict = dict({})):

    url = f"{api_url[country]}/api/v3/order/get_simple_order_ids"

    header = {
        "user-agent": user_agent
    }

    res = requests.get(url, params=data, headers=header, cookies=cookies,
                            timeout=time_out)

    api_logger(url, "get simple order ids", "", res)

    if SUCCESS_CODE == res.status_code:
        return res
    else:
        return False


# 通过ids组获取订单列表信息
def get_compact_order_list_by_order_ids(data: dict, country, cookies: dict = dict({})):

    url = f"{api_url[country]}/api/v3/order/get_compact_order_list_by_order_ids"

    header = {
        "user-agent": user_agent
    }

    res = requests.get(url, params=data, headers=header, cookies=cookies,
                            timeout=time_out)

    api_logger(url, "get compact order list by order ids", "", res)

    if SUCCESS_CODE == res.status_code:
        return res
    else:
        return False

