# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 11:48
# @Module  : scripts
# @Author  : lin
# @File    : script_login.py
"""
describe:

"""

from . import BaseScriptApplication, user_login, logging, appcation_logger, json, traceback


class LoginApplication(BaseScriptApplication):

    app_id = 1

    app_name = "登录应用服务"

    def run(self, args_opt):

        # 账号
        account = args_opt.account

        # 密码
        pwd = args_opt.password

        # 站点
        country = args_opt.country

        if not args_opt.accounts:
            # 登录单个
            self.login(account, pwd, country)
        else:
            # 批量登录多个账号
            try:
                accounts = json.loads(args_opt.accounts)

                for account in accounts:
                    self.login(account['account'], account['password'], account['country'])
            except Exception as e:
                appcation_logger(self.app_id, self.app_name, f"批量登录出现异常:{traceback.format_exc()}", logging.ERROR)

    def login(self, account, pwd, country):

        # 登录
        login_info = user_login(account, pwd, country)

        if not login_info:
            appcation_logger(self.app_id, self.app_name, f"账号:{account} 登录失败******", logging.ERROR)
        else:
            appcation_logger(self.app_id, self.app_name, {"account": account, "login_success": login_info})
