#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-04-22 14:03:51
LastEditTime: 2021-12-13 00:14:16
Description: file content
'''
from sqlalchemy import Column, String, JSON, Text
from app.models.base import Base, db


# 预测结果
class PredictionResult(Base):
    __tablename__ = 'prediction_result'

    hash = Column(String(128), nullable=False, unique=True, index=True)
    data = Column(JSON(), nullable=False)
    input_text = Column(Text(), nullable=False)

    @property
    def _required_fields(self):
        return ["hash", "data", "input_text"]
