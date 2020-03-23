import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import sqlite3

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app,database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db


class Movie(db.Model):
    __table__name = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    duration = db.Column(db.Integer)
    actors = db.relationship('Actor', backref='movies',nullable=True)

    def __repr__(self):
        return json.dumps(self.title)

class Actor(db.Model):
    __table__name = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    family_name = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def __repr__(self):
        return json.dumps(self.first_name + "_"+ self.family_name)



"""
* Database:
    * Refactor from Coffeeshop (just for the start use the sqlite3)
    * Create the Models
        * Movie: 
            * Title (str):
            * Duration (int)
            * Actor (object)
        * Actor:
            * first_name(str):
            * family name (str):
            * Movies (linked)
"""


sql_cmd2 = '''


SELECT * FROM movies;
'''
db.session.execute("""create table actors (
  id serial primary key,
  first_name varchar,
  last_name varchar
);""")

def create_sqlite3_db(database_filename):
    database_filename
    conn = sqlite3.connect(database_filename)
    print("database was created at following path",os.getcwd())
    return conn

def sqlite3_insert_data(conn):
    sql_cmd_list = [
        '''
            create table actors (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
              first_name varchar,
              last_name varchar
            );
        ''',
        '''
            create table movies (
              it INTEGER PRIMARY KEY AUTOINCREMENT,
              title varchar,
              duration integer,
              actor_id integer references actors(id)
            );
        ''',
        '''
            INSERT INTO actors (first_name,last_name) VALUES ('Franky','GOES');
        ''',
        '''
            INSERT INTO movies (title,duration,actor_id) VALUES ( 'Franky Goes',120,
                                                                         (Select id from actors where first_name='Franky')
                                                                        )
        '''
    ]
    for cmd in sql_cmd_list:
        conn.execute(cmd)
        conn.commit()

    conn.execute("Select * from actors").fetchall()

conn = create_sqlite3_db("database.db")
sqlite3_insert_data(conn)

import os
os.chdir(os.getcwd()+"//src")
database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

conn = _sqlite3.connect(database_path)