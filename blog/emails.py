#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emails.py - 2021/11/4
#
from threading import Thread

from flask import current_app, url_for
from flask_mail import Message

from blog.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


# noinspection PyUnresolvedReferences,PyProtectedMember
def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post, comment):
    # Locate to comments
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_mail(subject='新评论', to=current_app.config['BLOG_EMAIL'],
              html=f"""
              <p>您的文章：<b>{post.title}</b>&nbsp;有新的评论</p><hr>
              <p>来自&nbsp;<b>{comment.author}</b>&nbsp;的评论：</p>
              <p>{comment.body}</p><hr>
              <p>点击以下链接查看详情：</p>
              <p><a href="{post_url}">{post_url}</a></p>
              <p><small style="color: #868e96">该邮件为机器发送，请勿回复。</p>
              """)


def send_new_reply_email(post, comment):
    # Locate to comments
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_mail(subject='新回复', to=comment.replied.email,
              html=f"""
              <p>您评论过的文章&nbsp;<b>{post.title}</b>&nbsp;有新的回复：</p><hr>
              <p>来自&nbsp;<b>{comment.author}</b>&nbsp;的回复：</p>
              <p>{comment.body}</p><hr>
              <p>点击以下链接查看详情：</p>
              <p><a href="{post_url}">{post_url}</a></p>
              <p><small style="color: #868e96">该邮件为机器发送，请勿回复。</p>
              """)
