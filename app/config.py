import os

basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(basedir, '.env'))


class BaseConfig:
    TESTING = False
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'randomkey')
    # mail-related configs
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
    MAIL_PORT = os.getenv('MAIL_SERVER_PORT', 2525)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # stripe
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'randomkey')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'randomkey')
    STRIPE_WEBHOOK_KEY = os.getenv('STRIPE_WEBHOOK_KEY', 'randomkey')
    # errors monitoring
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    # redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RQ_REDIS_URL = REDIS_URL
    RQ_DASHBOARD_REDIS_URL = RQ_REDIS_URL


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True
    ASSET_DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    STRIPE_WEBHOOK_KEY = 'whsec_test_secret'
    ASSET_DEBUG = True
    # disable redis in test env
    RQ_ASYNC = False
    RQ_CONNECTION_CLASS = 'fakeredis.FakeStrictRedis'


class ProdConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')


configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}

