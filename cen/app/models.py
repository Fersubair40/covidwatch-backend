from app import db
from config import CEN_LENGTH


class CEN(db.Model):
  uuid = db.Column(db.String(CEN_LENGTH), primary_key=True, unique=True)
  created = db.Column(db.DateTime, server_default=db.func.now())

  def save(self):
    db.session.add(self)
    db.session.commit()

  def to_json(self) -> dict:
    return {'uuid': self.uuid, 'created': self.created}
