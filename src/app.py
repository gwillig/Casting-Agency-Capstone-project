import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import src.models
from src.models import setup_db,Actor,Movie,starredMovie
from sqlalchemy import inspect
import json

def create_app(dbms="sql", test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db ="test"

    if dbms == "sql":
        database_filename = "database.db"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
        db = setup_db(app, database_path)

    ###========= Insert data into data base if empty
    if db.session.query(Actor).count() == 0:
        src.models.insert_data(db)
    print(db.session.query(Actor).all())

    CORS(app)


    @app.route('/')
    def index():
        print("hello world")
        return "Welcome to the Casting Agency"


    @app.route('/actors', methods=['GET'])
    def get_all_actors():
        """
        Return all actors

        :return:
        """
        #Convert sqlalchemy  object into dict
        queryResult = [convert_sqlalchemy_todict(x) for x in db.session.query(Actor).all()]

        return jsonify({
            'success': True,
            'actors': queryResult
        }, 200)

    @app.route('/movies', methods=['GET'])
    def get_all_movies():
        """
        Return all actors

        :return:
        """
        #Convert sqlalchemy  object into dict
        queryResult = [convert_sqlalchemy_todict(x) for x in db.session.query(Movie).all()]

        return jsonify({
            'success': True,
            'movies': queryResult
        }, 200)

    @app.route("/movie/<string:movie_title>", methods=['Delete'])
    def delete_movie(movie_title):

        try:
            db.session.query(Movie).filter_by(title=movie_title).delete()
            db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
            abort(400)
        finally:
            db.session.close()

        return jsonify({
            'success': True
        },204)

    @app.route("/actor/<string:actor_name>", methods=['Delete'])
    def delete_actor(actor_name):
        first_name, family_name =actor_name.split("|")
        try:
            db.session.query(Actor).filter_by(first_name=first_name,family_name=family_name).delete()
            db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
            abort(400)
        finally:
            db.session.close()

        return jsonify({
            'success': True
        },204)

    @app.route("/actor", methods=['Patch'])
    def patch_actor():
        try:
            request_dict = request.form
            id = request_dict["id"]
            first_name = request_dict["first_name"]
            family_name = request_dict["family_name"]
            query_result = db.session.query(Actor).filter_by(id=id)
            if query_result.count() == 0:
                return jsonify({
                    'success': False
                }, 404)
            else:
                query_result.first_name = first_name
                query_result.family_name = family_name
                db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
            abort(404)
        finally:
            db.session.close()

        return jsonify({
            'success': True
        },204)
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
    def convert_sqlalchemy_todict(obj):
        """
        Converts a sqlalchemy oject to a dict
        :param obj:
        :return:
        """
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}

    return app, db
if __name__ == '__main__':
    APP, db = create_app()
    APP.run(host='0.0.0.0', port=8080, debug=True)