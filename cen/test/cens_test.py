from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from app.models import CEN
from datetime import datetime, timedelta
import json
import uuid
from config import CEN_LENGTH

URL_PATH = ''


def populate_db(db: SQLAlchemy) -> datetime:
  '''
  Populate the db with random CEN and return a datetime from before
  they were created.
  '''
  now = datetime.now()
  for i in range(10):
    new_cen = CEN(
        uuid=uuid.uuid4().hex, created_at=str(now - timedelta(days=i)))
    db.session.add(new_cen)
  db.session.commit()
  return now


def test_get_no_since_param(test_cli: FlaskClient, test_db: SQLAlchemy):
  response = test_cli.get('/api/v1/cens/')
  assert response.status_code == 400


def test_get_since_param(test_cli: FlaskClient, test_db: SQLAlchemy):
  then: datetime = populate_db(test_db)

  # Should return all 10
  response = test_cli.get(f'/api/v1/cens/?since={str(then)}')
  assert len(json.loads(response.data)['cens']) == 10

  # Should return 0
  response = test_cli.get(
      f'/api/v1/cens/?since={str(datetime.now() + timedelta(seconds=30))}')
  assert len(json.loads(response.data)['cens']) == 0


def test_post_no_param(test_cli: FlaskClient, test_db: SQLAlchemy):
  response = test_cli.post('/api/v1/cens/', content_type='application/json')
  assert response.status_code == 400


def test_post_uuid_wrong_len(test_cli: FlaskClient, test_db: SQLAlchemy):
  # Too short
  response = test_cli.post(
      f'/api/v1/cens/',
      data=json.dumps({
          'cens': [{
              'uuid': uuid.uuid4().hex,
              'created_at': str(datetime.now())
          }, {
              'uuid': uuid.uuid4().hex[:-1],
              'created_at': str(datetime.now())
          }]
      }),
      content_type='application/json')
  assert response.status_code == 400

  response = test_cli.post(
      f'/api/v1/cens/',
      data=json.dumps({
          'cens': [{
              'uuid': uuid.uuid4().hex,
              'created_at': str(datetime.now())
          }, {
              'uuid': uuid.uuid4().hex + uuid.uuid4().hex,
              'created_at': str(datetime.now())
          }]
      }),
      content_type='application/json')
  assert response.status_code == 400


def test_post_cens(test_cli: FlaskClient, test_db: SQLAlchemy):
  new_uuid1 = uuid.uuid4().hex
  new_uuid2 = uuid.uuid4().hex
  res = test_cli.post(
      f'/api/v1/cens/',
      data=json.dumps({
          'cens': [{
              'uuid': new_uuid1,
              'created_at': str(datetime.now())
          }, {
              'uuid': new_uuid2,
              'created_at': str(datetime.now())
          }]
      }),
      content_type='application/json')
  assert res.status_code == 201
  cens = CEN.query.all()
  assert len(cens) == 2
  assert cens[0].uuid == new_uuid1
  assert cens[1].uuid == new_uuid2
