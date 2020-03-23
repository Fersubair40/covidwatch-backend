from app import db
from config import CEN_LENGTH
from flask_sqlalchemy import SQLAlchemy


class CEN(db.Model):
  uuid = db.Column(db.String(CEN_LENGTH), primary_key=True, unique=True)
  created_at = db.Column(db.DateTime, nullable=False)
  publsihed_at = db.Column(
      db.DateTime, nullable=False, server_default=db.func.now())

  def to_json(self) -> dict:
    return {
        'uuid': self.uuid,
        'created_at': self.created_at,
        'published_at': self.publsihed_at
    }
