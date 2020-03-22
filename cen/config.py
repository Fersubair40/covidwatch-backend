import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  '''
  Parent configuration class.
  '''

  SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
  '''
  Configurations for Development.
  '''
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')


class TestingConfig(Config):
  '''
  Configurations for Testing, with a separate test database.
  '''
  TESTING = True
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


class StagingConfig(Config):
  '''
  Configurations for Staging.
  '''
  DEBUG = True


class ProductionConfig(Config):
  '''
  Configurations for Production.
  '''
  DEBUG = False
  TESTING = False


app_config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

CEN_LENGTH = 16