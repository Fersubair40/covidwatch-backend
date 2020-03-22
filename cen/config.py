import os
basedir = os.path.abspath(os.path.dirname(__file__))

API_VERSION = "1"


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
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/covidwatch-backend-test'


class StagingConfig(Config):
  '''
  Configurations for Staging.
  '''
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


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

CEN_LENGTH = 32