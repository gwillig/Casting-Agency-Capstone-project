####################################################
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    family_name = db.Column(db.String(50))

    movies = relationship("Movie", secondary="starredMovies")

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

    actors = relationship("Actor", secondary="starredMovies")


class starredMovie(db.Model):
    __tablename__ = 'starredMovies'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

    actor = relationship(Actor, backref=backref("starredMovies", cascade="all, delete-orphan"))
    movie = relationship(Movie, backref=backref("starredMovies", cascade="all, delete-orphan"))

##==================== app.py
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# create and configure the app
app = Flask(__name__)
# db = SQLAlchemy()
sql = True
if sql == True:
    database_filename = "database.db"
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)
db.create_all()
###=========
c1 = Actor(first_name="joe",family_name="normal")
db.session.add(c1)
db.session.commit()
##====
print(db.session.query(Actor).first())
