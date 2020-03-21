from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str) -> Flask:
  app = Flask(__name__)
  app.config.from_object(app_config[config_name])

  # register routes
  from app.routes import route_blueprint
  app.register_blueprint(route_blueprint)

  # register db
  db.init_app(app)
  # register migration
  migrate.init_app(app, db)

  return app
