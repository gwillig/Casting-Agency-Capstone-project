import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import src.models
from src.models import setup_db, Actor, Movie, starredMovie
from sqlalchemy import inspect
from src.auth import requires_auth
import json


def process_request(request):
    """
    Check if the parametre are in forms or in args
    :param request:
    :return:
    """
    if len(request.form) == 0:
        request_dict = request.args
    else:
        request_dict = request.form
    return request_dict


def create_app(dbms="sql", test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if dbms == "sql":
        if test_config == True:
            database_filename = "database_test.db"
        else:
            database_filename = "database.db"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
        db = setup_db(app, database_path)

    '1.Step: config cors'
    CORS(app)

    @app.route('/')
    def index():
        return "Welcome to the Casting Agency"

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_all_actors(payload):
        """
        Return all actors

        :return:
        """
        # Convert sqlalchemy  object into dict
        queryResult = [convert_sqlalchemy_todict(x) for x in db.session.query(Actor).all()]

        return jsonify({
            'success': True,
            'actors': queryResult
        }, 200)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_all_movies(payload):
        """
        Return all actors

        :return:
        """
        # Convert sqlalchemy  object into dict
        queryResult = [convert_sqlalchemy_todict(x) for x in db.session.query(Movie).all()]

        return jsonify({
            'success': True,
            'movies': queryResult
        }, 200)

    @app.route('/actor', methods=['GET'])
    @requires_auth('get:actor')
    def get_actor(payload):
        """
        Return all actors

        :return:
        """
        request_dict = process_request(request)
        actor_id = request_dict["id"]
        # Convert sqlalchemy  object into dict
        queryResult = convert_sqlalchemy_todict(db.session.query(Actor).filter_by(id=actor_id).first())

        return jsonify({
            'success': True,
            'actors': queryResult
        }, 200)

    @app.route('/movie', methods=['GET'])
    @requires_auth('get:movie')
    def get_movie(payload):
        """
        Return all actors

        :return:
        """
        request_dict = process_request(request)
        movie_id = request_dict["id"]
        # Convert sqlalchemy  object into dict
        queryResult = convert_sqlalchemy_todict(db.session.query(Movie).filter_by(id=movie_id).first())

        return jsonify({
            'success': True,
            'actors': queryResult
        }, 200)

    @app.route("/movie", methods=['Delete'])
    @requires_auth('delete:movie')
    def delete_movie(payload):

        try:
            request_dict = process_request(request)
            movie_title = request_dict["title"]
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
        }, 204)

    @app.route("/actor", methods=['Delete'])
    @requires_auth('delete:actor')
    def delete_actor(payload):

        request_dict = process_request(request)
        first_name = request_dict["first_name"]
        family_name = request_dict["family_name"]
        try:
            db.session.query(Actor).filter_by(first_name=first_name, family_name=family_name).delete()
            db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
            abort(400)
        finally:
            db.session.close()

        return jsonify({
            'success': True
        }, 204)

    @app.route("/actor", methods=['Patch'])
    @requires_auth('patch:actor')
    def patch_actor(payload):
        try:
            request_dict = process_request(request)
            actor_id = request_dict["id"]
            first_name = request_dict["first_name"]
            family_name = request_dict["family_name"]
            query_result = db.session.query(Actor).filter_by(id=actor_id)
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
        }, 204)

    @app.route("/actor", methods=['Post'])
    @requires_auth('post:actor')
    def post_actor(payload):
        # try:
        request_dict = process_request(request)
        movie_title = request_dict["movie_title"]
        first_name = request_dict["first_name"]
        family_name = request_dict["family_name"]

        query_result = db.session.query(Movie).filter_by(title=movie_title).first()
        a1 = Actor(first_name=first_name, family_name=family_name)
        query_result.actors.append(a1)
        db.session.commit()
        # except:
        #     db.session.rollback()
        #     db.session.close()
        #     abort(400)
        # finally:
        db.session.close()

        return jsonify({
            'success': True
        }, 204)

    @app.route("/movie", methods=['Patch'])
    @requires_auth('patch:movie')
    def patch_movie(payload):
        try:
            request_dict = process_request(request)
            movie_id = request_dict["id"]
            title = request_dict["title"]
            query_result = db.session.query(Movie).filter_by(id=movie_id)
            if query_result.count() == 0:
                return jsonify({
                    'success': False
                }, 404)
            else:
                query_result.title = title
                db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
            abort(404)
        finally:
            db.session.close()

        return jsonify({
            'success': True
        }, 204)

    @app.route("/movie", methods=['Post'])
    @requires_auth('post:movie')
    def post_movie(payload):
        try:
            request_dict = process_request(request)
            m1 = Movie(title=request_dict["title"])
            db.session.add(m1)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
            abort(404)
        finally:
            db.session.close()

        return jsonify({
            'success': True
        }, 204)

    """
    * API:

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

    return app


APP = create_app()

if __name__ == '__main__':
    APP = create_app()
    APP.run(host='0.0.0.0', port=8080, debug=True)
