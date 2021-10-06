#!/usr/bin/env python
# -*- coding: utf-8 -*-
# extensions.py - 2021年 十月 03日
#
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
moment = Moment()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from blog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录！'
login_manager.login_message_category = 'warning'
