#!/usr/bin/env python
# -*- coding: utf-8 -*-
# blog.py - 2021年 十月 01日
#
from flask import render_template, Blueprint, request, current_app, url_for, flash, redirect, abort, make_response
from flask_login import current_user

from blog.emails import send_new_reply_email, send_new_comment_email
from blog.extensions import db
from blog.forms import AdminCommentForm, CommentForm
from blog.models import Post, Comment, Category
from blog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about-me')
def about_me():
    post = Post.query.filter_by(title='关于我').first()
    if post:
        return render_template('blog/about.html', post=post)
    else:
        abort(404)


@blog_bp.route('/about-site')
def about_site():
    post = Post.query.filter_by(title='关于本站').first()
    if post:
        return render_template('blog/about.html', post=post)
    else:
        abort(404)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    # 更新阅读数
    post.readings = post.readings + 1
    db.session.add(post)
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_COMMENT_PER_PAGE']
    # 获取评论
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp).paginate(
        page, per_page)
    comments = pagination.items

    # 区别管理员和访客的评论表单
    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    # 提交评论
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        # 判断是否是回复评论
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            # 发邮件给被评论的人
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        # 管理员评论，无需发邮件
        if current_user.is_authenticated:
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed.', 'info')
            # 发邮件给管理员
            send_new_comment_email(post)
        return redirect(url_for('.show_post', post_id=post_id))

    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('Comment is disabled.', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLOG_THEMES']:
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response
