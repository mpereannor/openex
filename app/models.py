from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional
from uuid import UUID, uuid4
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login

Base = declarative_base()
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: so.Mapped[UUID] = so.mapped_column(
        sa.String(64), 
        default=lambda:str(uuid4()),
        primary_key=True
        )
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    account_number: so.Mapped[UUID] = so.mapped_column(sa.String(64), index=True, default=lambda: str(uuid4()), nullable=True)
    user_transactions: so.WriteOnlyMapped['Transaction'] = so.relationship(back_populates='client')
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?id=identicon&s={size}'

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return db.session.get(User, int(id))


@login.user_loader
def load_user(id): 
    return db.session.get(User, int(id))   

class Account(db.Model):
    __tablename__ = 'accounts'
    number: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, index=True, autoincrement=True)
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    normal: so.Mapped[int] = so.mapped_column(sa.BigInteger)

    def __repr__(self):
        return f'<Account #{self.name}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id: so.Mapped[UUID] = so.mapped_column(default=lambda: str(uuid4()), index=True, primary_key=True)
    transaction_id: so.Mapped[int] = so.mapped_column(sa.Integer, index=True, autoincrement=True)
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    amount: so.Mapped[int] = so.mapped_column(sa.Integer)
    direction: so.Mapped[int] = so.mapped_column(sa.BigInteger)
    description: so.Mapped[str] = so.mapped_column(sa.String(64))
    client: so.Mapped[User] = so.relationship(back_populates='user_transactions')
    user_id: so.Mapped[UUID] = so.mapped_column(sa.ForeignKey('users.id'), index=True)
    account_id: so.Mapped[int] = so.mapped_column( sa.ForeignKey('accounts.number'), index=True)
    second_account_id: so.Mapped[int] = so.mapped_column( sa.ForeignKey('accounts.number'), index=True)

    def __repr__(self):
        return f'<Transaction #{self.transaction_id}>'





