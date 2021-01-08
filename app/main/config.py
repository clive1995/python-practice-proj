import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '0Ngu@Rd_N3Xt+GeN3RaT10n')
    DEBUG = False


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    MONGODB_SETTINGS = {'DB': 'devconnector_test'}
    SECRET_KEY = '#test123'


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    MONGODB_SETTINGS = {'DB': 'devconnector_live'}
    SECRET_KEY = 'flask+mongoengine=<3'


config_by_name = dict(
    DEV=DevelopmentConfig,
    TEST=TestingConfig
)

key = Config.SECRET_KEY
