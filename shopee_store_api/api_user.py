# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : shopee_sotre_api
# @Author  : lin
# @File    : api_user.py
"""
describe:

    用户资源api

"""


from . import api_url, SUCCESS_CODE, time_out, user_agent, requests, logging, api_logger, traceback
import time


# 请求登录接口
def login(data: dict, country, cookies: dict = dict({})):

    url = f"{api_url[country]}/api/v2/login/"

    header = {
        "user-agent": user_agent
    }

    res = requests.post(url, data=data, headers=header, cookies=cookies,
                        timeout=time_out)

    api_logger(url, "login", "", res)

    if SUCCESS_CODE == res.status_code:
        return res
    else:
        return False

