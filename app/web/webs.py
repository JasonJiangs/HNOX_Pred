#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-04-20 15:15:01
LastEditTime: 2021-12-13 20:21:33
Description: file content
'''
import msgpack  # noqa
from flask import current_app
from app.utils.status_code import StatusCode
from flask import g
from . import web
from flask.templating import render_template
import os
from app.models.prediction_result import PredictionResult


@web.before_request
def before_request():
    g.sc = StatusCode()
    g.isDev = current_app.debug


@web.route('/', methods=['GET'])
def index():
    return render_template('index.html', data=dict(router="index", title="Home"))


# 预测结果
@web.route('/predictionResult/<string:hash>', methods=['GET'])
def prediction_result(hash):
    print(hash, current_app.config.get('PROJECT_ROOT_DIR'))
    res = PredictionResult.query.filter_by(hash=hash).first()
    files = dict(result_colored="",
                 result_color="",
                 result_noncolored="")
    if res:
        path_result = os.path.join(current_app.config.get(
            'PROJECT_ROOT_DIR'), "app", "static", "result_data", hash)
        base = f"/static/result_data/{hash}"
        if os.path.exists(os.path.join(path_result, "result_colored.xlsx")):
            files["result_colored"] = f"{base}/result_colored.xlsx"
        if os.path.exists(os.path.join(path_result, "result_color.csv")):
            files["result_color"] = f"{base}/result_color.csv"
        if os.path.exists(os.path.join(path_result, "result_noncolored.csv")):
            files["result_noncolored"] = f"{base}/result_noncolored.csv"

    return render_template('prediction_result.html',
                           data=dict(router="predictionResult",
                                     title="Prediction Result",
                                     res=res.data if res else [],
                                     files=files))
