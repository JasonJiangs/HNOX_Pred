#!/usr/bin/env python3
# coding=UTF-8
import os

class Config:
    SECRET_KEY = "bjCqR4GsQpUCvD4PwzFTZmGqJbpSe42i"
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@127.0.0.1:3306/hnoxpred?charset=utf8'
    # 动态追踪修改设置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_POOL_SIZE = 1024
    SQLALCHEMY_POOL_TIMEOUT = 90
    SQLALCHEMY_POOL_RECYCLE = 3
    SQLALCHEMY_MAX_OVERFLOW = 1024

    TEMPLATES_AUTO_RELOAD = True
    PROJECT_ROOT_DIR = os.path.abspath(
        os.path.dirname(os.path.dirname(__file__)))

    # SQLALCHEMY_ECHO = True
