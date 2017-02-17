class Config(object):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite://:memory:'

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
