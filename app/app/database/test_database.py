import unittest


class DatabaseTestSuite(unittest.TestCase):

    def test_basic(self):
        num = 2 + 2
        self.assertEqual(num, 4, "num is not Four")

