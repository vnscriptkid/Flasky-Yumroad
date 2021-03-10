class BaseConfig:
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    pass


configurations = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}

