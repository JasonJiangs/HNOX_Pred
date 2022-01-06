#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-12-07 10:01:40
LastEditTime: 2021-12-13 18:57:48
Description: file content
'''

from app.utils.status_code import StatusCode
from flask import g, jsonify, current_app
from app.utils.decorator import parse_json
from typing import Dict
from . import api
from app.HNOX_Pred.Prediction import run
import os
from app.models.prediction_result import PredictionResult
import traceback


@api.before_request
def before_request():
    g.sc = StatusCode()


# 执行预测
@api.route('/submitPrediction', methods=['POST'])
@parse_json
def prediction(data: Dict):
    print(data)
    hash = data.get('hash')
    input_text = data.get('inputValue')
    if not input_text or not hash:
        return jsonify(g.sc.args_missing)
    res = PredictionResult.query.filter_by(hash=hash).first()
    if res:
        return jsonify(g.sc.success('Successfully submit!'))  # 提交成功
    path_result = os.path.join(current_app.config.get(
        'PROJECT_ROOT_DIR'), "app", "static", "result_data", hash)
    try:
        res = run(path_result, hash, input_text)
        if not res:
            return jsonify(g.sc.custom_error("Wrong prediction, please check parameter!"))  # 预测错误请检查输入参数
        PredictionResult().add_object(PredictionResult, dict(
            data=res, hash=hash, input_text=input_text))

    except Exception as e:
        print(traceback.print_exc(), e)
        return jsonify(g.sc.custom_error(f"Prediction exception，{e}"))  # 预测异常

    return jsonify(g.sc.success('Successfully submit!'))  # 提交成功
