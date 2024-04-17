
from flask_babel import get_locale
from datetime import datetime, timezone
from flask_login import current_user, login_required 
from flask import render_template, g, request
from app.main import bp
from app import db

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
    g.locale = str(get_locale())

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home')
