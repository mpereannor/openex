from flask import url_for, jsonify, request
from flask_login import login_user, logout_user, current_user
import sqlalchemy as sa
from app import db
from app.auth import bp
from app.models import User
from app.auth.email import send_password_reset_email



@bp.route('/login', methods=[ 'POST'])
def login():
    data = request.json
    if data is None:
        return jsonify({'message': 'Bad Request'}), 400
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return jsonify({'message': 'Bad Request'}), 400

    user = db.session.scalar(
        sa.select(User).where(User.username == username))
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    login_user(user)
    return jsonify({'message': 'Login successful'}), 200


@bp.route('/logout')
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@bp.route('/register', methods=['POST'])
def register():
    data = request.json 
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

    if username is None or password is None or email is None:
        return jsonify({'error': 'Bad Request, Missing usernmae, email, or password'}), 400
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=username, email=email, firstname=firstname, lastname=lastname)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Registration successful, User created successfully.'}), 201



@bp.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    data = request.json
    email = data.get('email')
    
    if email is None:
        return jsonify({'error': 'Missing email'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        send_password_reset_email(user)
    
    return jsonify({'message': 'Instructions to reset your password have been sent to your email'}), 200



@bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    data = request.json
    password = data.get('password')
    
    if password is None:
        return jsonify({'error': 'Missing password'}), 400
    
    user = User.verify_reset_password_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    user.set_password(password)
    db.session.commit()
    
    return jsonify({'message': 'Your password has been reset'}), 200
