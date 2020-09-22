# -*- coding: utf-8 -*-
# @Time    : 2020/6/22 13:14
# @Author  : Ryu
# @Site    : 
# @File    : config.py.py
# @Software: PyCharm
import os
DEBUG = True
SECTET_KEY = os.urandom(24)
HOSTNAME = '127.0.0.1'
PORT = '3206'
DATABASE = 'message_board'
USENAME = 'root'
PASSWORD = 'lgh1519'
DB_URI = 'mysql + mysqldb:..{}:{}@{}:{}?charset=utf8'.format(USENAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLACHEMY_DATABASE_URI = DB_URI