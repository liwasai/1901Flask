import os
import sys

from flask import Flask,render_template
import click
from flask_sqlalchemy import SQLAlchemy#导入扩展类

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(app.root_path,'data.db')#Linux的四个/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.root_path,'data.db')#Windows的三个/
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #关闭了对模型修改的监控
db = SQLAlchemy(app)#初始化扩展，传入程序实例app

#modles
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

#views
@app.route('/')
# @app.route('/index')
# @app.route('/home')

def index():
    
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html',user=user,movies=movies)

# # 动态url
# @app.route('/index/<name>')
# def home(name):
#     return "<h1>hello,Flask,%s</h1>" %name



#自定义命令
@app.cli.command() #装饰器，注册命令
@click.option('--drop',is_flag=True,help='删除后再创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库完成')

#向data.db中写入数据的命令
@app.cli.command()
def forge():
    name = "中国"
    movies = [
        { "title" : "大赢家" , "year" : "2020" },
        { "title" : "叶问四" , "year" : "2020" },
        { "title" : "唐人街探案" , "year" : "2020" },
        { "title" : "囧妈" , "year" : "2020" },
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movies = Movie(title=m['title'],year=m['year'])
        db.session.add(movies)
    db.session.commit()
    click.echo('数据插入完成')

#错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    #返回模板和状态码
    return render_template('404.html',user=user),404

