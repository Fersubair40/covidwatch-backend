'''common fixtures to be used throughout the testing suite'''
import pytest
from flask import current_app
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from typing import Generator
from app import create_app, db


@pytest.fixture
def test_cli() -> Generator[FlaskClient, None, None]:
  '''
  Create app for testing session and yield client
  '''
  app = create_app('test')
  ctx = app.app_context()
  ctx.push()
  yield app.test_client()
  ctx.pop()


@pytest.fixture
def test_db() -> SQLAlchemy:
  '''
  Create all tables before each test and then remove all tables after each test
  '''
  db.create_all()
  yield db
  db.session.remove()
  db.drop_all()
