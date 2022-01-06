#!/usr/bin/env python3
# coding=UTF-8
'''
@Date: 2020-02-27 12:07:25
LastEditTime: 2021-04-22 09:43:42
@Description: file content
'''
from app import create_app
from app.models import db


app = create_app()

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=18181)
    # app.run(debug=True, host='0.0.0.0', port=18181)
