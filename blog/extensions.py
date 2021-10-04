#!/usr/bin/env python
# -*- coding: utf-8 -*-
# extensions.py - 2021年 十月 03日
#
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
