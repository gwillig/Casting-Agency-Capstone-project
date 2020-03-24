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
                                       "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FRkVPRE16UVVSRE16aENPVE" +
                                      "ZEUVRkR1FUVXpOVFpGTmtKRlJUbEZNemsyT1RWQ09FRTVRUSJ9.eyJpc3MiOiJodHRwczovL2" +
                                       "d3aWxsaWcuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1NTY1NDgyODE" +
                                       "4Mjc4OTAxNTMwIiwiYXVkIjpbImNhc3RpbmdfYWdlbmN5IiwiaHR0cHM6Ly9nd2lsbGlnLmV1" +
                                       "LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODUwNzgzMTEsImV4cCI6MTU4NTE2NDY5O" +
                                       "CwiYXpwIjoiUVltdW9ha2hiUERqQW1SRFB5ZnBnTGlsemNwV0ZBQUsiLCJzY29wZSI6Im9wZW" +
                                       "5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXR" +
                                       "lOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZSIsImdldDptb3Zp" +
                                       "ZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92a" +
                                       "WUiXX0.aufLPeJXyJ5GTHj8c4uV6THJ_k8jXOmyN3XKVf-xEdJAQWoRyt_BbYo0ZZxdIzAaVY" +
                                       "JoN4GLAbruYN6lanUzA_Ms4enP_GsUYJUDLNxhb5IwU6BSecTysM736YfGW5s3xSi75ps7UqP" +
                                       "UNgrckYopUIQSfj2PMYyq-WByPbfhz4wfXFwK-PfkX_XMVAtQLzFjHrU7m35BKCmZ9JgwmsEk" +
                                       "B-YoDv904v1qr91JY2_X3GZQJKcmK-PyOW58Z-62zpp9X550Bx4lGnwGATZDlHiUOty66DABk" +
                                       "WH9XNZMMy2SzcOYSJwmXm46mc3BBpK9c9vO0osMpn1pAbvHI6_T7BDt_Q"

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

    def test_404_error(self):
        # send request
        response = self.client().get('/patch', headers=self.header, data={"id": 1000})
        data = json.loads(response.data)

        '#1.Step: Check the error status and msg'
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_400_error(self):
        # send request
        response = self.client().delete('/actor', headers=self.header, data={})
        data = json.loads(response.data)

        '#1.Step: Check the error status and msg'
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_error(self):
        # send request
        response = self.client().post(
            '/actor', data=json.dumps({"1": 1}),
            headers = self.header,
            content_type='application/json')
        data = json.loads(response.data)

        '#1.Step: Check the error status and msg'
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'The server understands the content '
                         'type of the request entity')