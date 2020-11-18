import random
import time

from flask import session
from sqlalchemy import Table
from common.database import dbconnect
dbsession, md, DBase = dbconnect()

class User(DBase):
    __table__ = Table('user', md, autoload=True)
    def find_by_username(self, username):
        result = dbsession.query(User).filter_by(username=username).all()
        return result


    def find_by_userid(self, userid):
        row = dbsession.query(User).filter_by(userid=userid).first()
        return row

    def do_regisiter(self, username, password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        nickname = username.split('@')[0]
        avator = str(random.randint(1, 15))
        user =User(username=username, password=password, role='user', credit=50,
                   nickname=nickname, avator=avator + '.png', createtime=now, updatetime=now)
        dbsession.add(user)
        dbsession.commit()
        return user

    def update_credit(self, credit):
        user = dbsession.query(User).filter_by(userid=session.get('userid')).one()
        user.credit = int(user.credit) + credit
        dbsession.commit()

