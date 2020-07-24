# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:27:43 2020

@author: 23182
"""

import os
import sys
import click
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


WIN = sys.platform.startswith('win')
if WIN:  # 若windows系统,使用///
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修好的监控
db = SQLAlchemy(app)  # 初始化扩展,传入程序实例app.扩展类实例化前加载配置


class User(db.Model):
    '''表名将为user(自动生成，小写处理)'''
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    

class Movie(db.Model):
    '''表名将为movie(自动生成，小写处理)'''
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影


## 注册flask命令
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    '''设置选项'''
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initalized database.')  # 输出提示信息


@app.cli.command()
def forge():
    '''生成虚拟数据'''
    db.create_all()
    
    # 全局2个变量移至此处
    name = "NoCtwilight"
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
        
    db.session.commit()
    click.echo('Done')



## 注册路由
@app.route('/greet')
def hello():
    return "欢迎来到资源聚合网页！"

@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)







