import os


class BaseConfig:
    TESTING = False
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', '00000abcdef')


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

