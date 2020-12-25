# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : helper
# @Author  : lin
# @File    : helper_functions.py
"""
describe:

    内助助手函数;应用在运行或编译时可以不用引入包就能调用这里面的方法
    调用方式:在你任意执行代码的地方 直接以(helper.方法名)的形式调用,
    helper:当前这里的模板;
    方法名:当前helper里面的方法;

"""


import hashlib


# shopee密码加密登录
def password_hash_encryption(pwd: str):
    md5 = hashlib.md5(pwd.encode("utf-8")).hexdigest()
    password_hash = hashlib.sha256(md5.encode("utf-8")).hexdigest()
    return password_hash


# shopee请求头加安全哈希(基于md5)
def get_security_hash(plaintext: str, version: str):
    c = {
        "1": "396c15ad-6d3e-4018-98be-cef58cb45cd0",
        "2": "607c871d-b766-4c6f-ba89-b6c6ca32b156",
        "3": "42990074-9a73-4459-b749-f3110d222a72",
        "4": "5702b6f3-62a3-44d2-abe8-fece100a8bf4"
    }

    i = {
        "1": "70c74f4e-dcda-483e-826b-19dd2c42e799",
        "2": "29ffec18-c614-4645-8f1c-686e22d2e26a",
        "3": "04229e76-1ba3-4ac9-8a4e-68d46a3881a2",
        "4": "a3769a87-35cf-45e9-a5a7-2b4016c52e92"
    }

    if version in c.keys():
        plaintext_suffix = c[version]
    elif version in i.keys():
        plaintext_suffix = i[version]
    else:
        plaintext_suffix = ""

    md5 = hashlib.md5()
    md5.update((plaintext+plaintext_suffix).encode("utf-8"))

    return md5.hexdigest()


