import os


class BaseConfig:
    TESTING = False
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', '00000abcdef')
    # mail-related configs
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
    MAIL_PORT = os.getenv('MAIL_SERVER_PORT', 2525)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProdConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')


configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}

