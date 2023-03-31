import unittest
import requests

class TestApp(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5000"

    def test_hello_world(self):
        response = requests.get(f"{self.url}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello, World!")

if __name__ == "__main__":
    unittest.main()