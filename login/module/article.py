from sqlalchemy import Table, func
from common.database import dbconnect
from module.user import User

dbsession,md,DBase = dbconnect()

class Article(DBase):
    __table__ = Table('article', md, autoload=True)

    #查询所有文章
    def find_all(self):
        result = dbsession.query(Article).all()

    # 根据id查询文章
    def find_by_id(self, articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        return row

    # 指定分页的limit和offset的参数值，同时和用户表做连接
    def find_limit_with_user(self, start, count):
        result = dbsession.query(Article, User.nickname).join(User, User.userid == Article.userid)\
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1)\
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    def get_total_count(self):
        count = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1).count()
        return count

    def find_by_type(self, type, start, count):
        result = dbsession.query(Article, User.nickname).join(User, User.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.type == type) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    def get_count_by_type(self, type):
        count = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                                Article.type == type).count()
        return count


    def find_by_headline(self, headline, start, count):
        result = dbsession.query(Article, User.nickname).join(User, User.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                    Article.headline.like('%' + headline + '%')) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    def get_count_by_headline(self, headline):
        count = dbsession.query(Article).filter(Article.hidden == 0,
                                                Article.drafted == 0,
                                                Article.checked == 1,
                                                Article.headline.like('%' + headline + '%')).count()
        return count

    def find_last_9(self):
        result = dbsession.query(Article.articleid,Article.headline).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.articleid.desc()).limit(9).all()
        return result

    def find_most_9(self):
        result = dbsession.query(Article.articleid, Article.headline).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.readcount.desc()).limit(9).all()
        return result

    def find_recommended_9(self):
        result = dbsession.query(Article.articleid, Article.headline).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                                                             Article.recommended == 1 ) \
            .order_by(func.rand()).limit(9).all()
        return result

    def last_most(self):
        last = self.find_last_9()
        most = self.find_most_9()
        return last, most
