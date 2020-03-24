import unittest
import json
from src.app import create_app
from src.models import Movie, Actor, setup_db
import os

'''
Link to get token:
https://gwillig.eu.auth0.com/login?state=g6Fo2SBpUm8tOVA3WkFMc3djRTlEVkU4X0pyS1pvRjJuYVZaNqN0aWTZIG9PZlZad2JaczlQREhUWERxTWVtQnFuQ1BJSTBNUUIxo2NpZNkgUVltdW9ha2hiUERqQW1SRFB5ZnBnTGlsemNwV0ZBQUs&client=QYmuoakhbPDjAmRDPyfpgLilzcpWFAAK&protocol=oauth2&audience=casting_agency&response_type=token&redirect_uri=https://castingagencudacity.herokuapp.com/ 
'''


class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test cases"""

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""

        cls.header = {"Authorization": "Bearer " +
                                       "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FRkVPRE16UVVSRE16aENP" +
                                       "VEZEUVRkR1FUVXpOVFpGTmtKRlJUbEZNemsyT1RWQ09FRTVRUSJ9.eyJpc3MiOiJodHRwczovL2" +
                                       "d3aWxsaWcuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1NTY1NDgyODE4Mj" +
                                       "c4OTAxNTMwIiwiYXVkIjpbImNhc3RpbmdfYWdlbmN5IiwiaHR0cHM6Ly9nd2lsbGlnLmV1LmF1" +
                                       "dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODUwNTExMjYsImV4cCI6MTU4NTEzNzUxMywiY" +
                                       "XpwIjoiUVltdW9ha2hiUERqQW1SRFB5ZnBnTGlsemNwV0ZBQUsiLCJzY29wZSI6Im9wZW5pZ" +
                                       "CBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlO" +
                                       "m1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZSIsImdldDptb3ZpZ" +
                                       "XMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92a" +
                                       "WUiXX0.eKSZxOlWtWaA1V3SqTW8s9XP_F5qk4Xu0dD7sGI8DuySd_4TCGafMITAPXyvOcUGl3" +
                                       "PGB39F_cuDbHjcc0uwoOg06R-x3KweRzSUUvK9pRnmqf1V9P33LteYsyRAmM5xTj1fEA6jHk6F" +
                                       "v94m08teFLPTWlIsSnaqio1txqHWsEbLLFOrdVduKHc0XhpJ_pkXnrtTvMJCoZbxxkjP9pbYGg" +
                                       "o_Jo-aLhTQPX0_7R2RkJ1nLkBKhHszkDSubC9rJ6WNqEWsvHmZgiG1i0J07xyJjS9rYqRFOFOp" +
                                       "ZA4WGaa7ZpKVGV0k_8h_sWx00IlFF69U9lSATcWuppYRc4Drpu1l8g "
                      }

        cls.app = create_app(dbms="sql", test_config=True)
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}".format(os.path.join(project_dir, "database_test.db"))
        cls.db = setup_db(cls.app, database_path)
        cls.client = cls.app.test_client

        dummy_actor1 = Actor(first_name="Max", family_name="Mustermann")

        dummy_movie1 = Movie(title="Movie XY")
        dummy_movie1.actors.append(dummy_actor1)

        cls.db.session.bulk_save_objects(
            [
                Actor(first_name="Gerald", family_name="Mustermann"),
                Actor(first_name="Albert", family_name="Mustermann"),
                Actor(first_name="Max", family_name="Mustermann"),
                Movie(title="Doe goes New York"),
                Movie(title="Tim goes New York"),
                dummy_movie1
            ])

        cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        os.remove("database_test.db")

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_actors(self):
        response = self.client().get('/actors', headers=self.header)
        # response = self.client().get('/actors', headers={})
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]["success"], True)

    def test_get_actor(self):
        response = self.client().get(f'/actor', data={'id': 1}, headers=self.header)
        response_data: object = json.loads(response.data)
        self.assertEqual(response_data[1], 200)
        self.assertEqual(response_data[0]["success"], True)

    def test_get_movie(self):
        query_result = self.db.session.query(Movie).filter_by(title="Doe goes New York").first()
        response = self.client().get(f'/movie', data={"id": query_result.id}, headers=self.header)
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 200)
        self.assertEqual(response_data[0]["success"], True)

    def test_get_all_movies(self):
        response = self.client().get('/movies', headers=self.header)
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]["success"], True)

    def test_delete_movie(self):
        response = self.client().delete('/movie', data={"title": "Movie XY"}, headers=self.header)
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_delete_actor(self):
        response = self.client().delete('/actor', headers=self.header, data={"first_name": "Max",
                                                                             "family_name": "Mustermann"})
        response_data = json.loads(response.data)
        # Check response
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_patch_actor(self):
        query_result = self.db.session.query(Actor).filter_by(first_name="Gerald", family_name="Mustermann").first()
        response = self.client().patch('/actor', headers=self.header, data={"id": query_result.id,
                                                                            "first_name": "Franz",
                                                                            "family_name": "Mueller"})
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_post_actor(self):
        response = self.client().post('/actor', headers=self.header, data={
            "movie_title": "Tim goes New York",
            "first_name": "Hans",
            "family_name": "Gruber"
        })
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_patch_movie(self):
        query_result = self.db.session.query(Movie).filter_by(title='Doe goes New York').first()
        response = self.client().patch('/movie', headers=self.header, data={
            "id": query_result.id,
            "title": "Movie 12345",
        })
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)

    def test_post_movie(self):
        response = self.client().post('/movie', headers=self.header, data={
            "title": "Movie Hans goes to New York",
        })
        response_data = json.loads(response.data)
        self.assertEqual(response_data[1], 204)
        self.assertEqual(response_data[0]["success"], True)
