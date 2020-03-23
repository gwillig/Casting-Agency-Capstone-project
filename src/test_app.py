import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from src.app import create_app
from src.models import Movie, Actor


class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test cases"""

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""

        cls.app, cls.db = create_app(dbms="sql")
        cls.client = cls.app.test_client
        # binds the app to the current context
        with cls.app.app_context():
            cls.db = SQLAlchemy()
            cls.db.init_app(cls.app)
            # create all tables
            cls.db.create_all()
            dummy_actor1 = Actor(first_name="Max", family_name="Mustermann")
            dummy_actor2 = Actor(first_name="Gerald", family_name="Mustermann")
            dummy_movie = Movie(title="Movie XY")
            dummy_movie.actors.append(dummy_actor1)
            cls.db.session.add(dummy_movie)
            cls.db.session.add(dummy_actor2)
            cls.db.session.commit()


    def tearDown(self):
        """Executed after reach test"""
        pass



    def test_get_all_actors(self):
        response = self.client().get('/actors')
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]["success"], True)

    def test_get_all_movies(self):
        response = self.client().get('/movies')
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]["success"], True)

    def test_delete_movie(self):
        response = self.client().delete('/movie/Movie XY')
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_delete_actor(self):
        response = self.client().delete('/actor/Max|Mustermann')
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_patch_actor(self):
        query_result = ""
        with self.app.app_context():
            query_result = self.db.session.query(Actor).filter_by(first_name="Gerald", family_name="Mustermann").first()
        response = self.client().patch('/actor', data={"id":query_result.id,
                                                         "first_name":"Franz",
                                                         "family_name":"Mueller"})
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)
def manu_test():
    from urllib import request

    for path in ["","/actors"]:
        requ = request.urlopen("".join(["http://127.0.0.1:8080", path]))
        print(f"path: {path}, status: {requ.status}")

