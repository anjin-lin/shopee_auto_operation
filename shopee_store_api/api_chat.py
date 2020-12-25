# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 10:37
# @Module  : shopee_sotre_api
# @Author  : lin
# @File    : api_chat.py
"""
describe:

    聊天api

"""


from . import api_url, SUCCESS_CODE, time_out, user_agent, requests, logging, api_logger, traceback, json


# 发送消息
def messages(data: dict, country, chat_login_info, cookies: dict = dict({})):
    url = f"{api_url[country]}/webchat/api/v1.2/messages?_uid={chat_login_info['user']['uid']}&_v=4.7.0"

    header = {
        "authorization": "Bearer " + chat_login_info['token'],
        "content-type": "text/plain;charset=UTF-8",
        "user-agent": user_agent,
        "x-s": helper.get_security_hash(f"/messages?_uid={chat_login_info['user']['uid']}&_v=4.7.0",
                                                                    str(chat_login_info['version'])),
        "x-v": str(chat_login_info['version'])
    }

    res = requests.post(url, data=json.dumps(data), headers=header,
                        timeout=time_out)

    api_logger(url, "send messages", "", res)

    if SUCCESS_CODE == res.status_code:
        return res
    else:
        return False


# 登录聊天模块
def chat_login(data, country, cookies: dict = dict({})):

    url = f"{api_url[country]}/webchat/api/v1.2/login"

    header = {
        "user-agent": user_agent
    }

    res = requests.post(url, data=data, headers=header, cookies=cookies,
                        timeout=time_out)

    api_logger(url, "chat login", "", res)

    if SUCCESS_CODE == res.status_code:
        return res
    else:
        return False


