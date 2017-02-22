class Config(object):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite://:memory:'
    SESSION_TYPE = 'filesystem'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'false'

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
