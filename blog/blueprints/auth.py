#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth.py - 2021年 十月 01日
#
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'This is login page'


@auth_bp.route('/logout')
def logout():
    return 'Logout'
