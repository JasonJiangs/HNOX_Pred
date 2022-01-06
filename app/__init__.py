#!/usr/bin/env python3
# coding=UTF-8
'''
Date: 2021-03-23 11:50:22
LastEditTime: 2021-12-07 11:41:29
Description: file content
'''

from flask import Flask
from app.models.base import db
from app.settings import Config


def register_api_blueprint(app):
    from app.api import api
    app.register_blueprint(api, url_prefix='/api')
    from app.web import web
    app.register_blueprint(web, url_prefix='/')


def create_app(config=None):
    app = Flask(__name__)

    #: load default configuration
    app.config.from_object(Config)
    db.init_app(app)
    register_api_blueprint(app)
    return app
