# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : scripts
# @Author  : lin
# @File    : __init__.py
"""
describe:

    应用模块,业务代码应用,在这个模块当中,每个py文件
    都应是一个独立的应用,如果有业务需要多个py文件时
    建议在此模块中以包(package)的形式出现,确保
    应用(py文件业务)之间的独立.

"""

from shopee_store_api import *
from database.redis import get_redis
from database.mongodb import get_mongodb
from abc import ABCMeta, abstractmethod
import json
import argparse
import logging
from prettytable import PrettyTable
from collections import Counter
import traceback


redis_prefix = "shopee:"  # redis前缀

redis_obj = get_redis()  # 获取redis实例

login_effective_time = 86400  # 登录有效时间


script_log_name = "application"


# 应用服务日志
def appcation_logger(app_id, app_name, msg, level=logging.INFO):

    log_data = {
        "app_id": app_id,
        "app_name": app_name,
        "module": "scripts",
        "msg": msg
    }

    log_data = json.dumps(log_data)

    if level == logging.DEBUG:
        get_logger(script_log_name).debug(log_data)
    elif level == logging.INFO:
        get_logger(script_log_name).info(log_data)
    elif level == logging.ERROR:
        get_logger(script_log_name).error(log_data)
    elif level == logging.WARNING:
        get_logger(script_log_name).warning(log_data)


# 检测是否登录,
def check_login(account: str):
    login_info = redis_obj.get(f"{redis_prefix}login:{account}")

    if not login_info:
        return False
    else:
        return json.loads(login_info)


# 登录账号写入redis
def user_login(account: str, password: str, country):
    data = {
        "captcha_key": "",
        "remember": False,
        "password_hash": helper.password_hash_encryption(password),
        "username": account,
    }

    # 发起登录请求
    login_res = login(data, country)

    # 登录失败
    if not login_res:
        return False

    # 登录信息json反序列化
    login_json = json.loads(login_res.text)

    # 组装数据
    login_info = {
        "user_agent": user_agent,
        "account": account,
        "password": password,
        "login_result": login_json,
        "cookies": utils.dict_from_cookiejar(login_res.cookies)
    }

    # 登录信息写入redis
    redis_obj.setex(f"{redis_prefix}login:{account}", login_effective_time, json.dumps(login_info))

    return login_info


# 应用程序基类(抽象类)
class BaseScriptApplication(metaclass=ABCMeta):

    @property
    @abstractmethod
    def app_id(self) -> int:  # 应用标识 ID
        pass

    @property
    @abstractmethod
    def app_name(self) -> str:  # 应用名称
        return str()

    @abstractmethod
    def run(self, args_opt):
        pass


from .script_login import LoginApplication  # 账号登录应用服务
from .script_expediting import ExpeditingApplication  # 订单催付应用服务


# 脚本应用启动
class ScriptApplication(object):

    def __init__(self):
        self.application_container = []

        applications = BaseScriptApplication.__subclasses__()

        for application in applications:
            self.application_container.append({
                "app_id": application.app_id,
                "app_name": application.app_name,
                "application": application
            })

        self.argparses = argparse.ArgumentParser(description=os.getenv("PROJECT_NAME", ""))

    def start(self):
        # 获取命令行参数
        args_opt = self.command()

        application = None

        app_ids = [app['app_id'] for app in self.application_container]

        app_ids = dict(Counter(app_ids))

        app_repeat = [str(key) for key, value in app_ids.items() if value > 1]

        if 0 < len(app_repeat):
            print(f"检测到有重复应用ID: {','.join(app_repeat)}")
            exit()

        for app in self.application_container:
            if app['app_id'] == args_opt.application:
                application = app['application']
                break

        if not application:
            print(f"未找到 应用ID: {args_opt.application} 对应的应用服务")
            exit()

        appcation_logger(application.app_id, application.app_name, "启动应用===")

        # 应用启动
        application().run(args_opt)

    def command(self):
        account_info = self.argparses.add_argument_group()
        account_info.title = "用户账号信息"
        account_info.description = "针对于单用户操作"
        account_info.add_argument("--account", "-a", nargs="?", type=str, help="用户账号")
        account_info.add_argument("--password", "-p", nargs="?", default=None, type=str, help="用户密码")
        account_info.add_argument("--country", "-c", nargs="?",
                                  choices=[country for country in api_url],
                                  type=str, help="国家站点: \
                                                        th:泰国,id:印尼,my:马来,br:巴西,sg:新加坡,ph:菲律宾,vn:越南")
        self.argparses.add_argument("--accounts", "-as", nargs="?", type=str, help="多个账号信息,json格式：' \
                                                    '[{'account': '账号1', 'password': '密码1', 'country': '国家站点1'},'\
                                                    '{'account': '账号2', 'password': '密码2', 'country': '国家站点2'}]")
        self.argparses.add_argument("--other", "-other", nargs="+", type=str, help="传递给应用的其他信息")
        self.argparses.add_argument("--application", "-app", nargs="?", type=int, help="传递应用服务编号,启动应用")
        self.argparses.add_argument("apps", action='store_true', default=False, help="查看应用服务列表")

        return self.command_handler()

    # 查看应用列表
    def see_applications(self):

        app_list = PrettyTable()
        app_list.field_names = ["应用标识ID", "应用服务名"]
        for app in self.application_container:
            app_list.add_row([app['app_id'], app['app_name']])
        print(app_list)

    # 处理命令行参数
    def command_handler(self):
        args = sys.argv[1:]
        if len(args) <= 0:
            self.argparses.print_help()
            exit()

        if args[0] == 'apps':
            self.see_applications()
            exit()

        args_opt = self.argparses.parse_args()
        if args_opt.accounts is not None:
            pass
        elif not args_opt.account or not args_opt.password or not args_opt.country or not args_opt.application:
            self.argparses.error(r"add_argument: --account\-a, --password\-p, --country\c, --application\-app not None")

        return args_opt
