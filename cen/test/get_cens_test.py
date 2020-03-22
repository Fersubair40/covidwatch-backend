from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from app.models import CENs
from datetime import datetime, timedelta
import json
import uuid


def populate_db() -> datetime:
  '''
  Populate the db with random CENs and return a datetime from before
  they were created.
  '''
  now = datetime.now()
  for i in range(10):
    new_cen = CENs(uuid=uuid.uuid4().hex)
    new_cen.save()
  return now


def test_no_since_param(test_cli: FlaskClient, test_db: SQLAlchemy):
  response = test_cli.get('cens/')
  assert response.status_code == 400
  assert json.loads(response.data)['msg'] == 'Missing ?since=<datetime>'


def test_since_param(test_cli: FlaskClient, test_db: SQLAlchemy):
  then: datetime = populate_db()

  # Should return all 10
  response = test_cli.get(f'cens/?since={str(then)}')
  assert len(json.loads(response.data)['cens']) == 10

  # Should return 0
  response = test_cli.get(
      f'cens/?since={str(datetime.now() + timedelta(days=30))}')
  assert len(json.loads(response.data)['cens']) == 0