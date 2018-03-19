import unittest
import tempfile
from os import unlink, close
from ..main import app


class DatabaseTestSuite(unittest.TestCase):

    def setUp(self):
        # initialize temp databse file
        self.db_fd, app.config["DATABASE"] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.init_db()

    def tearDown(self):
        close(self.db_fd)
        unlink(app.config["DATABASE"])

    def login(self, email, password):
        """helper function"""
        return self.app.post("/login", data=dict(
            email=email,
            password=password
        ), follows_redirect=True)

    def logout(self):
        return self.app.get("/logout", follows_redirect=True)

    def register(self, name, email, password):
        return self.app.post("register", {
            "name": name,
            "email": email,
            "password": password
        }, follows_redirect=True)

    def test_empty_db(self):
        """validate that database is initialzed empty"""
        resp = self.app.get('/')
        self.assertEqual(resp.data, "No entries here so far")

    def test_login(self):
        resp = self.login('c234@citidel.com', 'morty')
        self.assertEqual(resp.data, "You're now logged in!")

    def test_logout(self):
        resp = self.logout()
        self.assertEqual(resp.data, "You have successfully logged out")

    def test_invalid_entry_handled(self):
        """
        test whether app properly handles
        invalid email and password entries
        """
        resp = self.login("c123@citidel.com", 'morty')
        self.assertEqual(resp.data, "Invalid Email")
        resp = self.login("c234@citidel.com", 'szechuansauce')
        self.assertEqual(resp.data, "Invalid Password")

    def test_registration(self):
        """
        validate registration endpoint
        function properly
        """
        resp = self.app.register('Rick', 'c234@citidel.com', 'morty')
        self.assertEqual(resp.data, "Registration was successful")

        # Note invalid email
        # resp = self.app.register("Rick", 'c234citidel.com', 'morty')
        # self.assertEqual(resp.data, "Registration was successful")

        # password to short
        # resp = self.app.register('Rick', 'c234@citidel.com', 'm')
        # self.assertEqual(resp.data, "Registration was successful")
