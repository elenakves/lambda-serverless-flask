import unittest
import sys
sys.path.append("..")
import custom_platform.app as app

# to test locally - run custom_platform/app.py
BASE_URL = 'http://127.0.0.1:5000/'

class TestHome(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_home(self):
        response = self.app.get(BASE_URL)

        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()