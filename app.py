# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:27:43 2020

@author: 23182
"""

import os
import sys
import click
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy


WIN = sys.platform.startswith('win')
if WIN:  # 若windows系统,使用///
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修好的监控
app.config['SECRET_KEY'] = 'dev'
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


@app.context_processor
def inject_user():
    '''模板上下文处理函数,函数名可随意设置'''
    user = User.query.first()
    return dict(user=user)  # 返回字典,即{'user': user}


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):
    '''接受异常对象作为参数'''
    return render_template('404.html'), 404  # 返回模板和状态码


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('输入内容无效')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('条目创建成功')
        return redirect(url_for('index'))
    
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=["GET", 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        
        if not title or not year or len(year)>4 or len(title)>60:
            flash('输入内容无效')
            return redirect(url_for('edit', movie_id=movie_id))
        
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('条目更新完成')
        return redirect(url_for('index'))
    
    return render_template('edit.html', movie=movie)
        

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('条目删除完成')
    return redirect(url_for('index'))




