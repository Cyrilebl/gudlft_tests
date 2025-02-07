import secrets


class Config:
    SECRET_KEY = secrets.token_hex(32)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test_secret_key"


class ProductionConfig(Config):
    DEBUG = False
