#!/usr/bin/env python
# -*- coding: utf-8 -*-
# utils.py - 2021/11/4
#
import os
from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for
from pygments.styles import get_all_styles


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def generate_styles():
    styles = list(get_all_styles())
    for style in styles:
        os.system(f'pygmentize -S {style} -f html -a .codehilite > {style}.css')


if __name__ == '__main__':
    generate_styles()
