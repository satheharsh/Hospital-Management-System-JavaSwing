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

    def test_login_api(self):
        response = self.client.post('/api/login', json={"username": "shrikar", "password": "431001"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get("success"))

    def test_add_and_discharge_patient_api(self):
        payload = {
            "id_type": "Aadhar Card",
            "id_number": "1234-9999-0000",
            "name": "API Patient",
            "gender": "Male",
            "disease": "Checkup",
            "deposit_amount": 4000.0
        }
        res_add = self.client.post('/api/patients', json=payload)
        self.assertEqual(res_add.status_code, 200)
        data_add = json.loads(res_add.data)
        self.assertTrue(data_add.get("success"))
        pid = data_add.get("patient_id")

        res_dis = self.client.post('/api/patients/discharge', json={"patient_id": pid, "amount_paid": 4000.0})
        self.assertEqual(res_dis.status_code, 200)
        data_dis = json.loads(res_dis.data)
        self.assertTrue(data_dis.get("success"))

    def test_book_ambulance_api(self):
        res = self.client.get('/api/ambulances')
        self.assertEqual(res.status_code, 200)
        ambs = json.loads(res.data)
        avail = [a for a in ambs if a.get("is_available")]
        if avail:
            amb_id = avail[0]["ambulance_id"]
            res_book = self.client.post('/api/ambulances/book', json={"ambulance_id": amb_id})
            self.assertEqual(res_book.status_code, 200)

if __name__ == "__main__":
    unittest.main()
