from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from flask import current_app, request
from . import login_manager
from flask import url_for
from app import app
import bleach
from markdown import markdown
import hashlib
import os
from app import config


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
    name = db.Column(db.String(64), nullable=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    about_me = db.Column(db.Text, nullable=True)
    # 注册时间
    member_since = db.Column(db.DateTime(), default=datetime.now)
    # 最后访问时间
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    # 头像hash值
    avatar_hash = db.Column(db.String(32))
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

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

    def gravatar(self, size=100, default='identicon', rating='g'):
        """
        根据email的hash值，获取用户头像
        :param size:
        :param default:
        :param rating:
        :return:
        """
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://secure.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, size=size, hash=hash,
                                                                     default=default, rating=rating)

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


# class Image(db.Model):
#     __tablename__ = 'images'
#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.String(255), nullable=False, default='')
#
#     @property
#     def image_path(self):
#         return '%s/%s' % (
#                 app.config['MEDIA_PATH'], self.image)
#
#     @property
#     def image_url(self):
#         if not self.image:
#             return None
#
#         return url_for('static', filename=self.image_path,
#                        _external=True)


# 实事要闻
class CurrentNews(db.Model):
    __tablename__ = 'current_news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    publish_time = db.Column(db.DateTime, default=datetime.now())
    img_path = db.Column(db.String(256), nullable=True)

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                      'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(bleach.clean(markdown(value, output='html'), tags=allow_tags, strip=True))

    @property
    def img_url(self):
        if self.img_path:
            return url_for('main.media', filename=self.img_path)
        else:
            return ''

db.event.listen(CurrentNews.content, 'set', CurrentNews.on_changed_content)


# 工作动态
class WorkTrends(db.Model):
    __tablename__ = 'work_trends'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    publish_time = db.Column(db.DateTime, default=datetime.now())
    img_path = db.Column(db.String(256), nullable=True)

    @property
    def img_url(self):
        if self.img_path:
            return url_for('main.media', filename=self.img_path)
        else:
            return ''

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                      'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(
                bleach.clean(markdown(value, output='html'), tags=allow_tags, strip=True))

db.event.listen(WorkTrends.content, 'set', WorkTrends.on_changed_content)


# 学习内容
class LearnContent(db.Model):
    __tablename__ = 'learn_contents'
    id = db.Column(db.Integer, primary_key=True)
    # 分类 0: 重要文件 1:理论学习 2:报刊社论
    classtype = db.Column(db.Integer)
    # 学习方式 0: 视频学习 1: 专题学习
    learntype = db.Column(db.Integer)
    # 标题
    title = db.Column(db.String(64), nullable=False)
    # 内容
    content = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    # 视频名称
    video_name = db.Column(db.String(256), default='')
    # 视频路径 todo 是否可以不存？？
    video_url = db.Column(db.String(256), default='')
    create_time = db.Column(db.DateTime, default=datetime.now())
    publish_time = db.Column(db.DateTime, default=datetime.now())

    # @staticmethod
    # def on_changed_content(target, value, oldvalue, initiator):
    #     allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
    #                   'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
    #     target.content_html = bleach.linkify(bleach.clean(markdown(value, output='html'), tags=allow_tags, strip=True))

    @classmethod
    def _names(cls):
        return [key for key in cls.__dict__.keys() if not key.startswith("_")]

    def _pack_data(self, isall=False):
        """
        将数据封装打包成字典格式
        :return:
        """
        result = {}
        for name in self._names():
            value = getattr(self, name)
            if name in ('create_time', 'publish_time'):
                if isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d")
            result[name] = value
        result['video_path'] = os.path.join('media', self.video_name)
        return result


# db.event.listen(LearnContent.content, 'set', LearnContent.on_changed_content)


# 活动集锦
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    publish_time = db.Column(db.DateTime, default=datetime.now())
    img_path = db.Column(db.String(256), nullable=True)

    @property
    def img_url(self):
        if self.img_path:
            return url_for('main.media', filename=self.img_path)
        else:
            return ''

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                      'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(
            bleach.clean(markdown(value, output='html'), tags=allow_tags, strip=True))


db.event.listen(Activity.content, 'set', Activity.on_changed_content)


# 党员风采
class PartyMember(db.Model):
    __tablename__ = 'party_members'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    publish_time = db.Column(db.DateTime, default=datetime.now())
    img_path = db.Column(db.String(256), nullable=True)

    @property
    def img_url(self):
        if self.img_path:
            return url_for('main.media', filename=self.img_path)
        else:
            return ''

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                      'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(bleach.clean(markdown(value, output='html'), tags=allow_tags, strip=True))


db.event.listen(PartyMember.content, 'set', PartyMember.on_changed_content)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    # 是否显示, 由管理员操作, False则不显示
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 评论对象的所对应在数据库中的表名， 比如party_members
    object_type = db.Column(db.String(32))
    # 评论对象的id
    object_id = db.Column(db.Integer)

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                      'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(
            bleach.clean(markdown(value, output='html'), tags=allow_tags, strip=True))

db.event.listen(Comment.content, 'set', Comment.on_changed_content)
