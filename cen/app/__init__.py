from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: Optional[str] = None) -> Flask:
  if config_name is None:
    config_name = os.getenv('APP_CONFIG')
    if config_name is None:
      raise RuntimeError("No config name specified")
  app = Flask(__name__)
  app.config.from_object(app_config[config_name])

  # register routes
  from app.routes import cens_blueprint
  app.register_blueprint(cens_blueprint, url_prefix='/cens')

  # register db
  db.init_app(app)
  # register migration
  migrate.init_app(app, db)

  # set up logging for prod and staging
  if config_name == "production" or config_name == "staging":
    if not os.path.exists('logs'):
      os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/cons.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('CONs app starting...')

  return app
