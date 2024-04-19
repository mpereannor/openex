from flask import Blueprint

bp = Blueprint('me', __name__)

from app.profile import routes