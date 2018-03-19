import unittest
from ..main import app

class AppTestSuite(unittest.TestCase):

    def test_index(self):
        # index endpoint process request normally
        test_client = app.test_client(self)
        resp = test_client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_database(self):
        """validate that database exists"""
        db_file = os.path.exists("ab.db")
        self.assertEqual(db_file, True)



