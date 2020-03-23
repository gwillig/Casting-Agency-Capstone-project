import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from src.app import create_app
from src.models import Movie, Actor

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""

        cls.app,db = create_app()
        cls.client = cls.app.test_client
        dummy_actor = Actor(first_name="Max",family_name="Mustermann")
        dummy_movie = Movie(title="Movie XY")
        dummy_movie.append(dummy_actor)
        db.session.add(dummy_movie)
        db.session.commit()


    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        response = self.client().get('/')
        print(response.data)

    def test_get_questions(self):
        response = self.client().get('/')
        print(response.data)


if __name__ == "__main__":
    unittest.main()