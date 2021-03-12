class BaseConfig:
    TESTING = False
    DEBUG = False
    WTF_CSRF_ENABLED = False


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    pass


configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}

