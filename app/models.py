from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from app import db


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
        sa.INTEGER(),
    )
    messages_sent: so.WriteOnlyMapped['Chat'] = so.relationship(
        foreign_keys='Chat.wrt_user', back_populates='author')
    messages_received: so.WriteOnlyMapped['Chat'] = so.relationship(
        foreign_keys='Chat.who', back_populates='recipient')


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
