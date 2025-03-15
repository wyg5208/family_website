from flask import Blueprint

bp = Blueprint('album', __name__)

from app.album import routes 