#!/usr/bin/env python3
# coding=UTF-8
'''
@Date: 2020-04-08 21:24:26
LastEditTime: 2021-12-07 10:20:48
@Description: file content
'''


from flask import request, g, jsonify

from functools import wraps


def parse_json(fun):
    @wraps(fun)
    def inner(*arg, **kwargs):
        input_data = request.json
        if not input_data:
            return jsonify(g.sc.args_missing)
        return fun(data=input_data, *arg, **kwargs)
    return inner
