# -*- coding: utf-8 -*-
# @Time    : 2020/5/15 16:33
# @Author  : Ryu
# @Site    : 
# @File    : hello.py.py
# @Software: PyCharm
from flask import Flask, render_template
import config
app = Flask(__name__)
app.config.from_object(config)

@app.route('/login.html')
def index():
    return render_template('login.html')
@app.route('/register.html')
def index_2():
    return render_template('register.html')
if __name__ == '__main__':
    app.run(debug=True)