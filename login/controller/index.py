import math

from flask import Blueprint, render_template, session, request

from module.article import Article
from module.user import User

index = Blueprint("index", __name__)


@index.route('/')
def home():
    article = Article()
    result = article.find_limit_with_user(0, 10)
    total = math.ceil(article.get_total_count() / 10)  # 总页数
    last, most = article.last_most()
    return render_template('index.html', result=result, page=1, total=total, last=last, most=most)


@index.route('/page/<int:page>')
def paginate(page):
    start = (page - 1) * 10
    article = Article()
    result = article.find_limit_with_user(start, 10)
    total = math.ceil(article.get_total_count() / 10)  # 总页数
    return render_template('index.html', result=result, page=page, total=total)


@index.route('/type/<int:type>-<int:page>')
def classify(type, page):
    article = Article()
    start = (page - 1) * 10
    result = article.find_by_type(type, start, 10)
    total = math.ceil(article.get_count_by_type(type) / 10)
    return render_template('type.html', result=result, type=type, page=page, total=total)


@index.route('/search/<int:page>-<keyword>')
def search(page, keyword):
    keyword = keyword.strip()
    if keyword is None or keyword == '' or '%' in keyword or len(keyword)>10:
        # abort(404)


        # 限制输入查询
        pass
    article = Article()
    start = (page - 1) * 10
    result = article.find_by_headline(keyword, start, 10)
    total = math.ceil(article.get_count_by_headline(keyword) / 10)
    return render_template('search.html', result=result, keyword=keyword, page=page, total=total)
