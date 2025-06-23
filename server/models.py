from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt
from datetime import datetime
from sqlalchemy import ForeignKey



class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-_password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String, unique=True ,nullable=False)
    password_hash = db.Column(db.String, nullable=False)

@hybrid_property
def password_hash(self):
    return self._password_hash

@password_hash.setter
def password_hash(self, password):
    self._password_hash = bcrypt.generate_password_hash(password.encode()).decode()

def authenticate(self, password):
    return self._password_hash and bcrypt.check_password_hash(self._password_hash, password.encode())


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column (db.String)
    episodes = relationship('Episode',back_populates='guest' cascade="all, delete ")


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer, db.DateTime, default=datetime.now)
    number = db.Column(db.Integer)
    guests = relationship('Guest', back_populates='episode')


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    guest_id = db.Column(db.Integer, ForeignKey('guests.id'))
    episode_id = db.Column(db.Integer, ForeignKey('episodes.id'))

    guest = relationship("Guest", back_populates="appearances")
    episode = relationship("Episode", back_populates="appearances")


@validates("rating")
def validating_instructions(self, key, rating):
    if rating is int > 5 :
         raise ValueError("rating must be between 1-5 ")
    return rating 






    