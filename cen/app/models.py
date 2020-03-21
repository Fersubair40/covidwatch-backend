from app import db
from config import CEN_LENGTH


class CEN(db.Model):
  id = db.Column(
      db.Integer, primary_key=True
  )  #TODO: Do we need id? Can just index by cen value since they should be unique?
  created = db.Column(db.DateTime, server_default=db.func.now())
  value = db.Column(db.String(CEN_LENGTH), index=True)