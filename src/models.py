import os

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
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))

    def __repr__(self):
        return json.dumps(self.title)

class Actor(db.Model):
    __table__name = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    family_name = db.Column(db.String)
    movie_id = db.relationship("Movie", backref="actors")

    def __repr__(self):
        return json.dumps(self.first_name + "_" + self.family_name)


# The following function are used to create a database (dbms: sqlite3) and insert data into the created data base
def create_sqlite3_db(database_filename):
    """
    Function to create a sqlite3 data base in the cwd
    :param database_filename (string): name of the database
    :return: conn (<class 'sqlite3.Connection'>)
    """
    database_filename
    if os.getcwd().split("/")[-1]=="src":
        os.chdir(os.getcwd()+"//src")
    conn = sqlite3.connect(database_filename)
    print("database was created at following path",os.getcwd())
    return conn

def excute_sqlite3_cmds(conn,sql_cmd_list):
    """
    Function execute sqlite3 cmds
    :param conn (<class 'sqlite3.Connection'>)
    :param sql_cmd_list (list): is a list of sqlite3 cmds
    """

    for index, cmd in enumerate(sql_cmd_list):
        print("Excute cmd no. ",index)
        conn.execute(cmd)
        conn.commit()

    print(conn.execute("Select * from actors").fetchall())

def  init_insert_sqlit3():
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
              id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    '#1.Step: Create a sqlite data base'
    conn = create_sqlite3_db("database.db")
    '#2.Step: Create the tables and insert data'
    excute_sqlite3_cmds(conn,sql_cmd_list)

init_insert_sqlit3()

####################################################
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))

    # ... any other fields

    create_dttm = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    products = relationship("Product", secondary="orders")

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    users = relationship("User", secondary="orders")


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    user = relationship(User, backref=backref("orders", cascade="all, delete-orphan"))
    product = relationship(Product, backref=backref("orders", cascade="all, delete-orphan"))



c1 = User(email="test@gmail.com")
db.session.add(c1)
db.session.commit()