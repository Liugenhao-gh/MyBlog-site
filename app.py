from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.orm import Query

import config
from models import  User ,Message
from exts import db
from decorators import login_required , center_to_index
from sqlalchemy import or_
from flask_sqlalchemy import BaseQuery
app = Flask(__name__)
app.config.from_object(config)
#在程序启动之前就注册
db.init_app(app)

#每页留言条数
per_page = 5

# 主页
@app.route('/')
def index():
    #获取页码数
    page = request.args.get('page',1)
    # 分页器对象
    query = Message.query.order_by(Message.create_time.desc())
    paginate = query.paginate(page=int(page), per_page=per_page)
    return render_template('index.html', paginate=paginate)

# 登录
@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        Email = request.form.get('Email')
        password = request.form.get('password')
        user = User.query.filter(User.Email == Email).first()
        if user and user.check_password(password):
            # 记录进入cookie
            session['user_id'] = user.id
            # 31天内不用再登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"用户名或密码错误，请确认后再登录。"

# 注册
@app.route('/regist/', methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        Email = request.form.get('Email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #如果Email被注册了，就不能再注册。
        user = User.query.filter(User.Email == Email).first()
        if user:
            return u"该Email已经被注册，请更换Email。"
        else:
            if password1!=password2:
                return  u"两次密码输入不一致。"
            else:
                user = User(Email=Email, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 注册成功，返回登录界面
                return redirect(url_for('login'))

#注销
@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

# 留言
@app.route('/leave/' , methods=['GET', 'POST'])
@login_required
def leave():
    if request.method == 'GET':
        return render_template('leave.html')
    else:
        content = request.form.get('message')
        num = len(content)
        if num <= 0:
            return u"留言内容不能为空。请重新填写。"
        elif num > 150:
            return u"留言内容不能超过150个字符。请重新填写。"
        else:
            user_id = session.get('user_id')
            user = User.query.filter(User.id == user_id).first()
            message = Message(message=content, author=user)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('index'))
# 查找
@app.route('/search/')
def search():
    q = request.args.get('q')
    page = request.args.get('page', 1)
    # 根据username和message查找
    users = User.query.filter(User.username.contains(q)).all()
    users_id =[]
    for user in users:
        users_id.append(user.id)
    if len(users_id)==0:
        users_id = [0]
    messages = Message.query.filter(or_(Message.message.contains(q), Message.author_id.contains(users_id))).order_by(Message.create_time.desc())
    paginate = messages.paginate(page=int(page), per_page=per_page)
    return render_template('search.html', paginate=paginate,q=q)

# 个人中心、管理自己的留言
@app.route('/MyCenter/')
def MyCenter():
    page = request.args.get('page',1)
    user_id = session.get('user_id')
    messages = Message.query.filter(Message.author_id.contains(user_id)).order_by(
        Message.create_time.desc())
    paginate = messages.paginate(page=int(page), per_page=per_page)
    return render_template('private.html', paginate=paginate)

# 删除自己的留言
@app.route('/delete/')
@center_to_index
def delete():
    message_id = request.args.get('message_id')
    message = Message.query.filter(Message.id == message_id).first()
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('MyCenter'))

# 钩子函数，上下文
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}

if __name__ == '__main__':
    app.run(Debug=True,host='0.0.0.0')
