# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:27:43 2020

@author: 23182
"""

from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return "欢迎来到资源聚合网页！"
