# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 10:00
# @Module  : config
# @Author  : lin
# @File    : config.py
"""
describe:

    基础配置

"""


from . import BaseConfig, os


class Config(BaseConfig):

    config_name = "default"

    @property
    def redis(self) -> dict:
        return {
            "host": os.getenv('REDIS_HOST', '127.0.0.1'),
            "port": int(os.getenv('REDIS_PORT', 6379)),
            "account": os.getenv('REDIS_ACCOUNT', ""),
            "password": os.getenv('REDIS_PASSWORD', ""),
            "database": 0
        }

    @property
    def log_info(self) -> dict:
        standard_format = '[%(levelname)s][%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s]' \
                          '\n[%(filename)s:%(lineno)d][%(message)s]'

        simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

        id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

        return {
                'version': int(os.getenv("LOG_VESION", 1)),
                # 禁用已经存在的logger实例
                'disable_existing_loggers': False,
                # 日志格式化(负责配置log message 的最终顺序，结构，及内容)
                'formatters': {
                    'distinct': {
                        'format': standard_format
                    },
                    'simple': {
                        'format': simple_format
                    },
                    'less_simple': {
                        'format': id_simple_format
                    },
                },
                # 过滤器，决定哪个log记录被输出
                'filters': {},
                # 负责将Log message 分派到指定的destination
                'handlers': {
                    # 打印到终端的日志
                    'console': {
                        'level': 'INFO',
                        'class': 'logging.StreamHandler',  # 打印到屏幕
                        'formatter': 'distinct'
                    },
                    # 打印到common文件的日志,收集info及以上的日志
                    'common': {
                        'level': 'INFO',
                        'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件
                        'formatter': 'simple',
                        'filename': './%s/sys_log.log' % os.getenv("LOG_PATH", "./logs"),       # 日志文件路径
                        # 'maxBytes': 1024*1024*5,  # 日志大小 5M
                        'backupCount': 5,   # 备份5个日志文件
                        'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                    },
                    # 应用服务日志
                    'application': {
                        'level': 'INFO',
                        'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件
                        'formatter': 'simple',
                        'filename': './%s/application.log' % os.getenv("LOG_PATH", "./logs"),  # 日志文件路径
                        # 'maxBytes': 1024*1024*5,  # 日志大小 5M
                        'backupCount': 5,  # 备份5个日志文件
                        'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                    },
                    # api日志
                    'api': {
                        'level': 'INFO',
                        'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件
                        'formatter': 'simple',
                        'filename': './%s/api.log' % os.getenv("LOG_PATH", "./logs"),  # 日志文件路径
                        # 'maxBytes': 1024*1024*5,  # 日志大小 5M
                        'backupCount': 5,  # 备份5个日志文件
                        'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                    },
                    # 打印到importance文件的日志,收集error及以上的日志
                    'importance': {
                        'level': 'ERROR',
                        'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件
                        'formatter': 'distinct',
                        'filename': './%s/sys_err.log' % os.getenv("LOG_PATH", "./logs"),  # 日志文件
                        # 'maxBytes': 1024*1024*5,  # 日志大小 5M
                        # 'maxBytes': 300,  # 日志大小 5M
                        'backupCount': 5, # 备份5个日志文件
                        'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                    },
                },
                # logger实例
                'loggers': {
                    # 默认的logger应用如下配置
                    'console': {
                        'handlers': ['console'],  # log数据打印到控制台
                        'level': 'DEBUG',
                        'propagate': True,  # 向上（更高level的logger）传递
                    },
                    'default': {
                        'handlers': ['console', 'common', 'importance'],
                        'level': 'INFO',
                        'propagate': True,  # 向上（更高level的logger）传递
                    },
                    'application': {
                        'handlers': ['application'],
                        'level': 'INFO',
                        'propagate': True,  # 向上（更高level的logger）传递
                    },
                    'api': {
                        'handlers': ['api'],
                        'level': 'INFO',
                        'propagate': True,  # 向上（更高level的logger）传递
                    },
                    'common': {
                        'handlers': ['console', 'common'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到控制台
                        'level': 'INFO',
                        'propagate': True,  # 向上（更高level的logger）传递
                    },
                    'importance': {
                        'handlers': ['console', 'importance'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到控制台
                        'level': 'ERROR'
                    },
                },
            }

    @property
    def mysql(self) -> dict:
        return {
            "host": os.getenv('MYSQL_HOST', '127.0.0.1'),
            "port": int(os.getenv('MYSQL_PORT', 3306)),
            "database": os.getenv('MYSQL_DATABASE', ""),
            "account": os.getenv('MYSQL_ACCOUNT', ""),
            "password": os.getenv('MYSQL_PASSWORD', ""),
        }

    @property
    def mongo(self) -> dict:
        return {
            "host": os.getenv('MONGODB_HOST', '127.0.0.1'),
            "port": int(os.getenv('MONGODB_PORT', 27017)),
            "database": os.getenv('MONGODB_DATABASE', ""),
            "account": os.getenv('MONGODB_ACCOUNT', ""),
            "password": os.getenv('MONGODB_PASSWORD', ""),
        }









