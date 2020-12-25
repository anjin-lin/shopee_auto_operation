# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 10:58
# @Module  : scripts
# @Author  : lin
# @File    : script_expediting.py
"""
describe:

    订单催付

"""

from . import BaseScriptApplication, \
    check_login, user_login, \
    logging, appcation_logger, get_simple_order_ids, get_compact_order_list_by_order_ids, \
    json, messages, chat_login, api_version

import uuid
import time


class ExpeditingApplication(BaseScriptApplication):

    app_id = 2

    app_name = "订单催付应用服务"

    def __init__(self):
        self.order_and_buyer_info = {}
        self.user_chat_login_info = {}
        self.expediting_content = "你TMD快点付钱啊！穷逼!!! 臭傻逼!!!"

    def run(self, args_opt):

        # 账号
        account = args_opt.account

        # 密码
        password = args_opt.password

        # 站点
        country = args_opt.country

        # 验证是否登录
        login_info = check_login(account)

        if not login_info:
            login_info = user_login(account, password, country)
            if not login_info:
                appcation_logger(self.app_id, self.app_name, f"账号:{account} 登录失败******", logging.ERROR)
                return False
            else:
                appcation_logger(self.app_id, self.app_name, {"account": account, "login_success": login_info})

        for order_info in self.get_order_info(login_info, country):
            user_id = order_info['buyer_user']['user_id']
            if user_id not in self.order_and_buyer_info.keys():
                self.order_and_buyer_info[user_id] = []
            self.order_and_buyer_info[user_id].append(order_info)

        # 执行催付
        self.expediting(login_info, country)

    # 向买家发起催付
    def expediting(self, login_info, country):
        for order_and_buyer in self.order_and_buyer_info:
            chat_login_info = None
            if login_info['account'] in self.user_chat_login_info.keys():
                chat_login_info = self.user_chat_login_info[login_info['account']]
            else:
                chat_login_info = self.get_chat_login_info(login_info, country)

            if not chat_login_info:
                continue

            count = 100

            while True:
                message_req_data = {
                    "request_id": str(uuid.uuid1()),
                    "to_id": int(order_and_buyer),
                    "type": "text",
                    "content": {"text": f"{self.expediting_content}{count}"},
                    "text": self.expediting_content,
                    "chat_send_option": {
                        "force_send_cancel_order_warning": False,
                        "comply_cancel_order_warning": False
                    }
                }

                msg_res = messages(message_req_data, country, chat_login_info, login_info['cookies'])

                if not msg_res:
                    appcation_logger(self.app_id, self.app_name, f"站点:{country} 账号:{login_info['account']} "
                                                                 f"买家：{order_and_buyer}"
                                                                 f"发起催付失败:{json.dumps(message_req_data)}",
                                     level=logging.ERROR)
                    print(f"向买家: {order_and_buyer} 发起催付失败******")
                    return False

                appcation_logger(self.app_id, self.app_name, f"站点:{country} 账号:{login_info['account']} "
                                                             f"买家：{order_and_buyer}"
                                                             f"成功发起催付:{msg_res.text}")
                print(f"向买家: {order_and_buyer} 成功发起催付......")
                count -= 1

                if count <= 0:
                    break

                time.sleep(2)

            return True

    # 获取订单信息(暂时只针对未付款订单催付)
    def get_order_info(self, login_info, country):

        simple_req_data = {
            "source": "unpaid",
            "page_size": 40,
            "page_number": 1,
            "total": 0,
            "is_massship": False,
            "from_page_number": 1
        }

        order_ids_res = get_simple_order_ids(simple_req_data, country, login_info['cookies'])

        while True:
            if not order_ids_res:
                appcation_logger(self.app_id, self.app_name, f"站点:{country} 账号:{login_info['account']} "
                                                             f"获取订单simple ids组失败:{json.dumps(simple_req_data)}",
                                 level=logging.ERROR)
                break
            order_ids_json = json.loads(order_ids_res.text)

            if not order_ids_json['data']['orders']:
                break

            appcation_logger(self.app_id, self.app_name, f"站点:{country} 账号:{login_info['account']} "
                                                         f"获取订单到simple ids组: {order_ids_res.text}",)

            order_req_data = {
                "order_ids": ",".join([str(order['order_id']) for order in order_ids_json['data']['orders']])
            }

            order_info_s = get_compact_order_list_by_order_ids(order_req_data, country, login_info['cookies'])

            if not order_info_s:
                appcation_logger(self.app_id, self.app_name, f"站点:{country} 账号:{login_info['account']} "
                                                             f"获取订单信息失败:{json.dumps(order_req_data)}",
                                                                                    level=logging.ERROR)
                continue
            order_info_s_json = json.loads(order_info_s.text)

            appcation_logger(self.app_id, self.app_name, f"站点:{country} 账号:{login_info['account']} "
                                                         f"获取订单到信息{order_info_s.text}",)

            for order_info in order_info_s_json['data']['orders']:
                yield order_info

            simple_req_data['page_size'] = order_ids_json['data']['page_info']['page_size']
            simple_req_data['page_number'] += 1
            simple_req_data['total'] = order_ids_json['data']['page_info']['total']
            simple_req_data['from_page_number'] = order_ids_json['data']['page_info']['page_number']
            order_ids_res = get_simple_order_ids(simple_req_data, country, login_info['cookies'])

    # 获取登录聊天模块信息,认证Shopee聊天模块
    def get_chat_login_info(self, login_info, country):

        chat_login_req_data = {
            "_uid": F"0-{login_info['login_result']['id']}",
            "_v": api_version
        }

        chat_login_res = chat_login(chat_login_req_data, country, login_info['cookies'])

        if not chat_login_res:
            appcation_logger(self.app_id, self.app_name, f"站点:{country} 账号:{login_info['account']} "
                                                         f"登录聊天模块失败:{json.dumps(chat_login_req_data)}",
                                                        level=logging.ERROR)
            return False
        else:
            appcation_logger(self.app_id, self.app_name, f"站点:{country} 账号:{login_info['account']} 登录聊天模块成功...",)
            chat_login_info = json.loads(chat_login_res.text)
            self.user_chat_login_info[login_info['account']] = chat_login_info

            return chat_login_info


