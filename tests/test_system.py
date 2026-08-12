from datetime import datetime
import os
import unittest

from models import Patient, Room, Employee, Department, Ambulance
from services.hospital_management_system import HospitalManagementSystem

class TestHospitalManagementSystem(unittest.TestCase):

    def setUp(self):
        self.hms = HospitalManagementSystem()

    def test_login(self):
        self.assertTrue(self.hms.login("shrikar", "431001"))
        self.assertFalse(self.hms.login("admin", "wrong"))

    def test_rooms_initialization(self):
        rooms = self.hms.get_all_rooms()
        self.assertGreater(len(rooms), 0)

    def test_add_and_find_patient(self):
        test_patient = Patient(
            patient_id="PTEST01",
            id_type="Aadhar Card",
            id_number="1234-5678-9012",
            name="Test Patient",
            gender="Male",
            disease="Fever",
            admission_time=datetime.now(),
            deposit_amount=5000.0
        )
        added = self.hms.add_patient(test_patient)
        self.assertTrue(added)

        retrieved = self.hms.find_patient_by_id("PTEST01")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Test Patient")

    def test_discharge_patient_frees_room(self):
        # Create test patient with assigned room
        room_num = "S1"
        test_patient = Patient(
            patient_id="PTEST02",
            id_type="Voter ID",
            id_number="VOTER999",
            name="Discharge Test",
            gender="Female",
            disease="Flu",
            admission_time=datetime.now(),
            deposit_amount=2000.0
        )
        test_patient.room_number = room_num
        self.hms.add_patient(test_patient)

        # Discharge patient
        success = self.hms.discharge_patient("PTEST02", 2000.0)
        self.assertTrue(success)

        # Verify room is available
        room = self.hms.find_room_by_number(room_num)
        if room:
            self.assertTrue(room.available)

    def test_add_patient_occupies_room(self):
        room_num = "S2"
        room = self.hms.find_room_by_number(room_num)
        if room:
            room.available = True
            self.hms.update_room(room)

        test_patient = Patient(
            patient_id="PTEST03",
            id_type="Aadhar Card",
            id_number="9999-8888-7777",
            name="Room Test",
            gender="Male",
            disease="Cold",
            admission_time=datetime.now(),
            deposit_amount=3000.0
        )
        test_patient.room_number = room_num
        self.hms.add_patient(test_patient)

        updated_room = self.hms.find_room_by_number(room_num)
        if updated_room:
            self.assertFalse(updated_room.available)

    def test_ambulance_booking_and_release(self):
        ambs = self.hms.get_available_ambulances()
        if ambs:
            amb_id = ambs[0].ambulance_id
            self.assertTrue(self.hms.book_ambulance(amb_id))
            self.assertTrue(self.hms.release_ambulance(amb_id))

    def test_discharge_pending_calculation(self):
        test_patient = Patient(
            patient_id="PTEST04",
            id_type="Aadhar Card",
            id_number="1111-2222-3333",
            name="Pending Test",
            gender="Female",
            disease="Injury",
            admission_time=datetime.now(),
            deposit_amount=5000.0
        )
        self.hms.add_patient(test_patient)
        self.hms.discharge_patient("PTEST04", 2000.0)

        retrieved = self.hms.find_patient_by_id("PTEST04")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.pending_amount, 3000.0)
        self.assertEqual(retrieved.amount_paid, 2000.0)

    def tearDown(self):
        # Clean up test patients
        self.hms.patient_dao.delete_patient("PTEST01")
        self.hms.patient_dao.delete_patient("PTEST02")
        self.hms.patient_dao.delete_patient("PTEST03")
        self.hms.patient_dao.delete_patient("PTEST04")

if __name__ == "__main__":
    unittest.main()
