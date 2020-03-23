import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from src.aa import create_app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""

        cls.app = create_app()
        cls.client = cls.app.test_client



    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions(self):
        response = self.client().get('/')
        print(response.data)


if __name__ == "__main__":
    unittest.main()