from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from app.models import CEN
from datetime import datetime, timedelta
import json
import uuid
from config import CEN_LENGTH


def populate_db() -> datetime:
  '''
  Populate the db with random CEN and return a datetime from before
  they were created.
  '''
  now = datetime.now()
  for i in range(10):
    new_cen = CEN(uuid=uuid.uuid4().hex)
    new_cen.save()
  return now


def test_get_no_since_param(test_cli: FlaskClient, test_db: SQLAlchemy):
  response = test_cli.get('cens/')
  assert response.status_code == 400
  assert json.loads(response.data)['msg'] == 'Missing ?since=<datetime>'


def test_get_since_param(test_cli: FlaskClient, test_db: SQLAlchemy):
  then: datetime = populate_db()

  # Should return all 10
  response = test_cli.get(f'cens/?since={str(then)}')
  assert len(json.loads(response.data)['cens']) == 10

  # Should return 0
  response = test_cli.get(
      f'cens/?since={str(datetime.now() + timedelta(days=30))}')
  assert len(json.loads(response.data)['cens']) == 0


def test_post_no_param(test_cli: FlaskClient, test_db: SQLAlchemy):
  response = test_cli.post('cens/')
  assert response.status_code == 400
  assert json.loads(response.data)['msg'] == 'Missing ?uuid=<uuid>'


def test_post_uuid_wrong_len(test_cli: FlaskClient, test_db: SQLAlchemy):
  # Too short
  response = test_cli.post(f'cens/?uuid={uuid.uuid4().hex[:-1]}')
  assert response.status_code == 400
  assert json.loads(
      response.data)['msg'] == f'uuid must be of length {str(CEN_LENGTH)}'

  # Too long
  response = test_cli.post(f'cens/?uuid={uuid.uuid4().hex + uuid.uuid4().hex}')
  assert response.status_code == 400
  assert json.loads(
      response.data)['msg'] == f'uuid must be of length {str(CEN_LENGTH)}'


def test_post_uuid(test_cli: FlaskClient, test_db: SQLAlchemy):
  new_uuid = uuid.uuid4().hex
  res = test_cli.post(f'cens/?uuid={new_uuid}')
  assert res.status_code == 201
  cens = CEN.query.all()
  assert len(cens) == 1
  assert cens[0].uuid == new_uuid
