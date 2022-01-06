#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-04-20 15:14:08
LastEditTime: 2021-12-07 11:40:53
Description: file content
'''
from flask import Blueprint


web = Blueprint('web', __name__, url_prefix='/')

from app.web import webs  # noqa
