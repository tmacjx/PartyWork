import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')

    # 管理员邮箱地址
    ADMIN_EMAIL = ""

    HOST = '127.0.0.1'
    # HOST = '0.0.0.0'
    PORT = 9000

    MAIL_SERVER = 'smtp.qq.com'

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')

    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SECRET_KEY = "test"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    PROJECT_PATH = basedir

    MEDIA_PATH = '/media'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'test': TestingConfig,
    'product': ProductConfig
}


