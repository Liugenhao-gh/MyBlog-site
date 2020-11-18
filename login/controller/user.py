import hashlib
import re

from flask import Blueprint, make_response, session, request, url_for
from common.unity import ImagCode, gen_email_code, send_email
from controller import index
from module.credit import Credit
from module.user import User

user = Blueprint('user', __name__)

@user.route('/vcode')
def vcode():
    code, bstring = ImagCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response

@user.route('/ecode', methods = ['POST'])
def ecode():
    email = request.form.get('email')
    if not re.match('.+@.+\..+', email):
        return 'email-invalid'
    ecode = gen_email_code()
    try:
        send_email(email, ecode)
        session['ecode'] = ecode
        return 'send-pass'
    except:
        return 'send-fail'

@user.route('/user', methods = ['POST'])
def register():
    user = User()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    code = request.form.get('code').strip()

    if code != session.get('ecode'):
        print(code, session.get('ecode'))
        return 'ecode-error'
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return 'up-invalid'

    elif len(user.find_by_username(username)) > 0:
        return 'user-repeated'
    else:
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.do_regisiter(username, password)
        print(result)
        session['islogin'] = 'true'
        session['userid'] = result.userid
        session['username'] = username
        session['nickname'] = result.nickname
        session['role'] = result.role

        Credit().insert_detail(type='用户注册', target='0', credit=50)
        return 'reg-pass'

@user.route('/login', methods = ['POST'])
def login():
    user = User()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('logincode').strip().lower()
    print(vcode, session.get('vcode'))

    if vcode != session.get('vcode') or vcode == 0000:
        return 'vcode-error'
    else:
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['islogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role
            # 更新积分表
            Credit().insert_detail(type='正常登录', target='0', credit=1)
            user.update_credit(1)
            # 写入cookie
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=1*3600)
            response.set_cookie('password', password, max_age=1*3600)
            return response
        else:
            return 'login-fail'

@user.route('/logout')
def logout():
    session.clear()

    response = make_response('注销并进行重定向', 302)
    response.headers['Location'] = url_for('index.home')
    response.delete_cookie('username')
    response.set_cookie('password', '', max_age=0)
    return response





