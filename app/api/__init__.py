#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-04-15 16:25:32
LastEditTime: 2021-04-15 16:27:53
Description: file content
'''
from flask import Blueprint


api = Blueprint('api', __name__, url_prefix='api')

from app.api import apis  # noqa
