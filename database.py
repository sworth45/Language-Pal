from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

user_data = {} # key=username, value=User_Data

class User_Data:
    favorites = []
    conversations = {} # key=language, value = list of conversations in a language
                       # each conversation will be the list of Message objects

class Message:
    from_user = False
    message = ""

user_data = {}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

"""
     # Relationship to favorited languages
    favorites = db.relationship('FavoriteLanguage', back_populates='user', cascade="all, delete-orphan")
    conversations = db.relationship('Conversation', back_populates='user', cascade="all, delete-orphan")

class FavoriteLanguage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='favorites')

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='conversations')
"""