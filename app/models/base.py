#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-03-23 10:53:17
LastEditTime: 2021-12-14 21:14:57
Description: file content
'''

from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer, DateTime
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Dict, List
__all__ = ['db', 'Base']


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception('%r' % e)
            if throw:
                raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    _create_time = Column(DateTime, default=datetime.now)
    _update_time = Column(DateTime, default=datetime.now)

    @property
    def create_time(self):
        return self._create_time.strftime(
            "%Y-%m-%d %H:%M:%S") if self._create_time else None

    @property
    def updated_time(self):
        return self._update_time.strftime(
            "%Y-%m-%d %H:%M:%S") if self._update_time else None

    @property
    def _required_fields(self):
        return []

    def set_attrs(self, attrs: Dict) -> None:
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def check_required_fields(self, form: Dict):
        return [i for i in self._required_fields if not form.get(i)]

    def add_object(self, obj: object, data: Dict) -> Dict:
        if not data:
            return g.sc.args_missing
        if self.check_required_fields(data):
            return g.sc.args_missing
        form = {key: value for key, value in data.items() if hasattr(obj, key)}
        try:
            obj = obj()
            obj.set_attrs(form)
            db.session.add(obj)
            db.session.commit()
            return g.sc.success()
        except Exception as e:
            print(e)
            db.session.rollback()
            return g.sc.system_inner_error

    def obj_to_json(self, obj: object):
        result = {}
        for i in dir(obj):
            val = obj.__getattribute__(i)
            if (not i.startswith('_') and not hasattr(val, '__call__')
                    and i != 'metadata' and not isinstance(val, Query)):
                try:
                    if isinstance(val, str) or isinstance(
                            val, int) or isinstance(val, bool) or isinstance(
                                val, dict) or isinstance(val, list):
                        result[i] = val
                    else:
                        result[i] = f"{val}" if val else ""
                except Exception as e:
                    print(e)
                    result[i] = None
        return result

    def get_json(self, obj_list: List[object]):
        data = []
        for i in obj_list:
            i = self.obj_to_json(i)
            if i:
                data.append(i)
        return data
