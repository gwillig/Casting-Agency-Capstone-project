import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from src.app import create_app
from src.models import Movie, Actor
import os

class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test cases"""

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""

        cls.app, cls.db = create_app(dbms="sql",test_config=True)
        cls.client = cls.app.test_client

        dummy_actor1 = Actor(first_name="Max", family_name="Mustermann")
        dummy_actor2 = Actor(first_name="Gerald", family_name="Mustermann")
        dummy_movie1 = Movie(title="Movie XY")
        dummy_movie2 = Movie(title="Doe goes New York")
        dummy_movie3 = Movie(title="Tim goes New York")
        dummy_movie1.actors.append(dummy_actor1)
        cls.db.session.add(dummy_movie1)
        cls.db.session.add(dummy_movie2)
        cls.db.session.add(dummy_movie3)
        cls.db.session.add(dummy_actor2)
        cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        os.remove("database_test.db")

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_actors(self):
        response = self.client().get('/actors')
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]["success"], True)


    def test_get_actor(self):
        query_result = self.db.session.query(Actor).filter_by(first_name="Gerald", family_name="Mustermann").first()
        response = self.client().get(f'/actor/{query_result.id}')
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 200)
        self.assertEqual(response_data[0]["success"], True)

    def test_get_movie(self):
        query_result = self.db.session.query(Movie).filter_by(title="Doe goes New York").first()
        response = self.client().get(f'/movie/{query_result.id}')
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 200)
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
        query_result = self.db.session.query(Actor).filter_by(first_name="Gerald", family_name="Mustermann").first()
        response = self.client().patch('/actor', data={"id":query_result.id,
                                                         "first_name":"Franz",
                                                         "family_name":"Mueller"})
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_post_actor(self):
        response = self.client().post('/actor', data={
                                                         "movie_title": "Tim goes New York",
                                                         "first_name": "Hans",
                                                         "family_name": "Gruber"
                                                         })
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)


    def test_patch_movie(self):
        query_result = self.db.session.query(Movie).filter_by(title='Doe goes New York').first()
        response = self.client().patch('/movie', data={
                                                         "id":query_result.id,
                                                         "title": "Movie 12345",
                                                         })
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_post_movie(self):
        response = self.client().post('/movie', data={
                                                         "title": "Movie Hans goes to New York",
                                                         })
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

def manu_test():
    from urllib import request

    for path in ["","/actors"]:
        requ = request.urlopen("".join(["http://127.0.0.1:8080", path]))
        print(f"path: {path}, status: {requ.status}")

