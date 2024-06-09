from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(UserMixin, db.Model):
    id_user: so.Mapped[int] = so.mapped_column(
        primary_key=True,
    )
    name: so.Mapped[str] = so.mapped_column(
        sa.String(64),
        index=True,
        unique=True,
    )
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120),
        index=True,
        unique=True,
    )
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256),
    )
    exp: so.Mapped[int] = so.mapped_column(
        sa.INTEGER(), default=0,
    )
    messages_sent: so.WriteOnlyMapped['Chat'] = so.relationship(
        foreign_keys='Chat.wrt_user', back_populates='author')
    messages_received: so.WriteOnlyMapped['Chat'] = so.relationship(
        foreign_keys='Chat.who', back_populates='recipient')
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
           return (self.id_user)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id_user, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return db.session.get(User, id)
    
    
@login.user_loader
def load_user(id_user):
    return db.session.get(User, int(id_user))



class Avatar(db.Model):
    id_ava: so.Mapped[int] = so.mapped_column(
        primary_key=True,
    )
    gander: so.Mapped[str] = so.mapped_column(
        sa.String(10),
    )
    vid: so.Mapped[str] = so.mapped_column(
        sa.String(30),
    )
    path: so.Mapped[str] = so.mapped_column(
        sa.String(30),
    )


class Chat(db.Model):
    id_msg: so.Mapped[int] = so.mapped_column(
        primary_key=True,
    )
    msg: so.Mapped[str] = so.mapped_column(
        sa.String(4000),
    )
    time_msg: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(
            timezone.utc,
        )
    )
    wrt_user: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id_user),
                                               index=True)
    who: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id_user),
                                               index=True)
    
    author: so.Mapped[User] = so.relationship(
        foreign_keys='Chat.wrt_user',
        back_populates='messages_sent')
    recipient: so.Mapped[User] = so.relationship(
        foreign_keys='Chat.who',
        back_populates='messages_received')


class Inventar(db.Model):
    id_inv: so.Mapped[int] = so.mapped_column(
        primary_key=True,
    )
    name_object: so.Mapped[str] = so.mapped_column(
        sa.String(52),
    )

class Quest(db.Model):
    id_quest: so.Mapped[int] = so.mapped_column(
        primary_key=True,
    )
    cont_quest: so.Mapped[str] = so.mapped_column(
        sa.Boolean(),
    )
