from flask import Blueprint, request
from app.models import CEN, db
from datetime import datetime
cens_blueprint = Blueprint('cens', __name__)
from config import CEN_LENGTH, API_VERSION
from typing import List
import json

PREFIX = "/api/v" + API_VERSION + '/cens'


@cens_blueprint.route(PREFIX + '/', methods=['GET', 'POST'])
def cens():
  if request.method == 'GET':
    since: str = request.args.get('since')
    if since is None:
      return ({
          'msg':
              'Missing ?since=<datetime> (utc datetime, i.e. "2020-03-22 16:40:31.989538"'
      }, 400)
    cens = CEN.query.filter(CEN.created >= since).all()
    return ({'cens': [cen.to_json() for cen in cens]}, 200)

  elif request.method == 'POST':
    cens: List[str] = request.get_json().get('cens')
    if cens is None or len(cens) == 0:
      return ({'msg': 'Missing list of cens'}, 400)
    for cen in cens:
      if len(cen) != CEN_LENGTH:
        return ({'msg': f'{cen} is not of expected length {CEN_LENGTH}'}, 400)
      cen = CEN(uuid=cen)
      db.session.add(cen)
    # Only save if ALL cens sent were valid
    db.session.commit()
    return ('', 201)