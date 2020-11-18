from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='templates', static_url_path='/', static_folder='resources')
app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234a@localhost:3306/zhihu?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.context_processor
def gettype():
    type = {
        '1': 'A',
        '2': 'B',
        '3': 'C',
        '4': 'D',
        '5': 'E'
    }
    return dict(article_type=type)


# 自定义truncate函数并注册
def truncate(s, length, end='...'):
    count = 0
    new = ''
    for c in s:
        new += c
        if ord(c) <= 128:
            count += 0.5
        else:
            count += 1
        if count > length:
            break
    return new + end


app.jinja_env.filters.update(truncate=truncate)

# 全局拦截器
@app.before_request
def before():
    url = request.path

    pass_list = ['/user', '/login', '/logout']
    if url in pass_list or url.endswith('.js') or url.endswith('.jpg'):
        pass
    elif session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username is not None and password is not None:
            user = User()
            result = user.find_by_username(username)
            if len(result) == 1 and result[0].password == password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role

if __name__ == '__main__':
    from controller.index import *

    app.register_blueprint(index)

    from controller.user import *

    app.register_blueprint(user)

    app.run(debug=True)
