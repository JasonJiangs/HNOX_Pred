#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-03-09 21:22:09
LastEditTime: 2021-03-27 22:35:36
Description: file content
'''

from datetime import datetime


def obj2json(obj):
    res = {}
    for i in dir(obj):
        try:
            val = obj.__getattribute__(i)
            if i != "metadata" and not i.startswith('_') and not hasattr(
                    val, '__call__') and i:
                data = getattr(obj, i)
                if (isinstance(data, datetime)):
                    res[i] = data.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    res[i] = data
        except Exception:
            # print(e)
            pass
    return res


def data2json(obj_list):
    data = []
    for i in obj_list:
        i = obj2json(i)
        if i:
            data.append(i)
    return data
