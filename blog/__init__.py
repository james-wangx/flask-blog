#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __init__.py - 2021年 十月 01日
#
import click
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from blog.blueprints.admin import admin_bp
from blog.blueprints.auth import auth_bp
from blog.blueprints.blog import blog_bp

app = Flask('blog')
app.config.from_pyfile('settings.py')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
ckeditor = CKEditor(app)
mail = Mail(app)
moment = Moment(app)

app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """
    初始化数据库
    """
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')

    db.create_all()
    click.echo('Initialized database.')