from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy


def test_hello(test_cli: FlaskClient, test_db: SQLAlchemy):
  response = test_cli.get('/')
  assert response.status_code == 200
