#!/usr/bin/env python
# -*- coding: utf-8 -*-
# blog.py - 2021年 十月 01日
#
from flask import Blueprint

blog_bp = Blueprint('blog_bp', __name__)


@blog_bp.route('/about')
def about():
    return 'The about page'


@blog_bp.route('/category/<int:category_id>')
def category(category_id):
    return 'The category page.'
