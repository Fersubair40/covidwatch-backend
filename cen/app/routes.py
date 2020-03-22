from flask import Blueprint, request
from app.models import CEN
from datetime import datetime
cens_blueprint = Blueprint('cens', __name__)
from config import CEN_LENGTH


@cens_blueprint.route('/', methods=['GET', 'POST'])
def cens():
  if request.method == 'GET':
    since: str = request.args.get('since')
    if since is None:
      return ({'msg': 'Missing ?since=<datetime>'}, 400)
    cens = CEN.query.filter(CEN.created >= since).all()
    return ({'cens': [cen.to_json() for cen in cens]}, 200)

  elif request.method == 'POST':
    uuid: str = request.args.get('uuid')
    if uuid is None:
      return ({'msg': 'Missing ?uuid=<uuid>'}, 400)
    if len(uuid) != CEN_LENGTH:
      return ({'msg': f'uuid must be of length {str(CEN_LENGTH)}'}, 400)
    cen = CEN(uuid=uuid)
    cen.save()
    return ('', 201)