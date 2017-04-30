from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from flask import current_app
from . import login_manager
from flask import url_for
from app import app


class Permission:
    """
    权限 暂分为 1.是否可以评论 2.是否是 管理员
    """
    COMMENT = 0x02
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_role():
        """
        初始化分配角色, 用于python shell下执行 新建 或者 更新  python manage.py shell
        :return:
        """
        roles = {
            'User': (Permission.COMMENT, True),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    # 注册时间
    member_since = db.Column(db.DateTime(), default=datetime.now)
    # 最后访问时间
    last_seen = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        数据库只存 hash加密过的密码
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions == permissions)

    @property
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    @property
    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# todo 可能存在 多个配图的情况 多对多？


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False, default='')

    @property
    def image_path(self):
        return '%s/%s' % (
                app.config['MEDIA_PATH'], self.image)

    @property
    def image_url(self):
        if not self.image:
            return None

        return url_for('static', filename=self.image_path,
                       _external=True)






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


# todo 评论？？