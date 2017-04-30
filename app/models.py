from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verity_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def is_admin(self):
        return True if Role.query.get(id=self.role_id).name == 'Admin' else False


from . import login_manager

#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

#
# # 实事要闻
# class CurrentNews(db.Model):
#     __tablename__ = 'current_news'
#     title = db.Column(db.String(64), nullable=False)
#     content = db.Column(db.text, nullable=True)
#     create_time = db.Column(db.Time, default=datetime.now())
#     publish_time = db.Column(db.Time, default=datetime.now())
#
#
# # 工作动态
# class WorkTrends(db.Model):
#     __tablename__ = 'work_trends'
#     title = db.Column(db.String(64), nullable=False)
#     content = db.Column(db.text, nullable=True)
#     create_time = db.Column(db.Time, default=datetime.now())
#     publish_time = db.Column(db.Time, default=datetime.now())
#
#
# # 学习内容
# class LearnContent(db.Model):
#     __tablename__ = 'learn_contents'
#     # 分类 0: 重要文件 1:理论学习 2:报刊社论
#     classtype = db.Column(db.Integer)
#     # 学习方式 0: 视频学习 1: 专题学习
#     learntype = db.Column(db.Integer)
#     # 标题
#     title = db.Column(db.String(64), nullable=False)
#     # 内容
#     content = db.Column(db.text, nullable=True)
#     # 视频名称
#     video_name = db.Column(db.String(64), default='')
#     # 视频路径 todo 是否可以不存？？
#     video_url = db.Column(db.String(64), default='')
#     create_time = db.Column(db.Time, default=datetime.now())
#     publish_time = db.Column(db.Time, default=datetime.now())
#
#
# # 活动集锦
# class Activity(db.Model):
#     __tablename__ = 'activities'
#     title = db.Column(db.String(64), nullable=False)
#     content = db.Column(db.text, nullable=True)
#     create_time = db.Column(db.Time, default=datetime.now())
#     publish_time = db.Column(db.Time, default=datetime.now())
#     # todo 是否支持图片上传
#
#
# # 党员风采
# class PartyMember(db.Model):
#     __tablename__ = 'party_members'
#     title = db.Column(db.String(64), nullable=False)
#     content = db.Column(db.text, nullable=True)
#     create_time = db.Column(db.Time, default=datetime.now())
#     publish_time = db.Column(db.Time, default=datetime.now())
#     # todo 是否支持图片上传？？
#
# # todo 评论？？