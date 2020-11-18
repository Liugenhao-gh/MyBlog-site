import time

from flask import session
from sqlalchemy import Table
from common.database import dbconnect
dbsession, md, DBase = dbconnect()

class Credit(DBase):
    __table__ =Table('credit', md, autoload=True)

    def insert_detail(self, type, target, credit):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=session.get('userid'), category=type, target=target, credit=credit
                        , createtime=now, updatetime=now)
        dbsession.add(credit)
        dbsession.commit()
