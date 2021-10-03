#!/usr/bin/env python
# -*- coding: utf-8 -*-
# settings.py - 2021年 十月 03日
#
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.db')

MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = ('Blog Admin', MAIL_USERNAME)

BLOG_EMAIL = os.getenv('BLOG_EMAIL')
BLOG_POST_PER_PAG = 10
BLOG_MANAGE_POST_PER_PAGE = 15
BLOG_COMMENT_PER_PAGE = 15
