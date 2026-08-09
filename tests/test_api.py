import json
import unittest
from app import app

class TestHospitalAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_api(self):
        response = self.client.get('/api/dashboard')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("total_patients", data)
        self.assertIn("available_rooms", data)

    def test_get_patients_api(self):
        response = self.client.get('/api/patients')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_rooms_api(self):
        response = self.client.get('/api/rooms')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
