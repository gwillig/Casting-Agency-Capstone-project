import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import src.models
from src.models import Movie, Actor
#================= Just for development


#======
from sqlalchemy import create_engine


from sqlalchemy import create_engine


#======================
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = SQLAlchemy()
    sql = True
    if sql==True:
        database_filename = "database.db"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    ##=======
    move_obj = Movie(title="Franky Goes", duration=120)
    actor_obj = Actor(first_name="Frank",family_name="Goes", movie_id=move_obj)

    db.session.add(move_obj)
    db.session.commit()


    CORS(app)
    return app

APP = create_app()
db = src.models.setup_db(APP)
@APP.route('/')
def index():
    return "Welcome to the Casting Agency"


@APP.route('/actor/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):
    """

    :param actor_id: id number of actor in the data base
    :return:
    """
    actor_obj = db.session.query(src.models.Actor).filter_by(id=actor_id).first()

    return jsonify({
        'success': True,
        'actor': actor_obj
    }, 200)
"""
* API:
    * GET /actors and /movies
    * DELETE /actors/ and /movies/
    * POST /actors and /movies and
    * PATCH /actors/ and /movies/
    * Testing:  
        * One test for success behavior of each endpoint
        * One test for error behavior of each endpoint
        * At least two tests of RBAC for each role


"""

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)