from flask import Blueprint, request
from app.models import CENs
from datetime import datetime
cens_blueprint = Blueprint('cens', __name__)


@cens_blueprint.route('/', methods=['GET', 'POST'])
def cens():
  if request.method == 'GET':
    since: str = request.args.get('since')
    if since is None:
      return {'msg': 'Missing ?since=<datetime>'}, 400
    cens = CENs.query.filter(CENs.created >= since).all()
    return {'cens': [cen.to_json() for cen in cens]}, 200
