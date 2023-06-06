"""
To create database models for users and notes.
"""
# . means we are importing from our app package i.e website __init.py
from . import db
from flask_login import UserMixin
# For time
from sqlalchemy.sql import func


# Model is a layout or blueprint for the object to be stored in the database
# To set up the Note Model
# To define schema of the note table.
# All of our notes should conform as below.
# In flask by default id is auto_increment
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Foreign key references column of one table to another
    # For One-to-many (one user can have many notes) relationship
    # In foreign key we pass lowercase table_name.column_name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# To set up the User model.
# To define schema of the user table.
# All of our Users should conform as below.
# In flask by default id is auto_increment
class User(db.Model, UserMixin):
    # primary key is id of type integer
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # We want to find all the notes of a user
    # this field will store the list of notes ids for each user
    # In relationship we pass class-name of the table
    notes = db.relationship('Note')
