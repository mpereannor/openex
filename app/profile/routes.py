from flask import jsonify, request, g
from app import db
from app.profile import bp
from app.models import User
from flask_babel import get_locale
from datetime import datetime, timezone
from time import time
from flask_login import login_user, logout_user, current_user, login_required


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
    g.locale = str(get_locale())

@bp.route('/', methods=['GET'])
@login_required
def view_profile():
    user = User.query.get(current_user.id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404

    # Serialize the user data
    serialized_user = {
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'about_me': user.about_me,
        'account_number': user.account_number,
        'email': user.email,
    }

    return jsonify(serialized_user), 200

from flask import request, jsonify

@bp.route('/', methods=['PUT'])
@login_required
def edit_user_profile():
    user = User.query.get(current_user.id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404

    data = request.json
    if 'username' in data:
        user.username = data['username']
    
    if 'firstname' in data:
        user.firstname = data['firstname']
    
    if 'lastname' in data:
        user.lastname = data['lastname']
    if 'about_me' in data:
        user.about_me = data['about_me']

    db.session.commit()

    return jsonify({ 'message': 'Profile updated successfully' }), 200
