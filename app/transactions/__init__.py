from flask import Blueprint

bp = Blueprint('tr', __name__)

from app.transactions import routes
