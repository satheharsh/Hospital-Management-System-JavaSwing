import csv
from datetime import datetime
import os
import subprocess
from typing import List, Optional

from models import Patient, Room, Employee, Department, Ambulance
from daos import PatientDAO, RoomDAO, EmployeeDAO, DepartmentDAO, AmbulanceDAO
from utils.database_initializer import DatabaseInitializer

class HospitalManagementSystem:
    DEFAULT_USERNAME = "shrikar"
    DEFAULT_PASSWORD = "431001"

    def __init__(self):
        DatabaseInitializer.initialize_database()

        self.room_dao = RoomDAO()
        self.patient_dao = PatientDAO()
        self.employee_dao = EmployeeDAO()
        self.department_dao = DepartmentDAO()
        self.ambulance_dao = AmbulanceDAO()

        self.rooms: List[Room] = self.room_dao.get_all_rooms()
        self.patients: List[Patient] = self.patient_dao.get_all_patients()
        self.departments: List[Department] = self.department_dao.get_all_departments()
        self.employees: List[Employee] = self.employee_dao.get_all_employees()
        self.ambulances: List[Ambulance] = self.ambulance_dao.get_all_ambulances()

        if not self.rooms:
            self._initialize_default_rooms()
        if not self.departments:
            self._initialize_default_departments()
        if not self.employees:
            self._initialize_default_employees()
        if not self.ambulances:
            self._initialize_default_ambulances()

    def _initialize_default_departments(self):
        depts = [
            Department("OPD", "1234567890"),
            Department("OT", "1234567891"),
            Department("Nursing Department", "1234567892"),
            Department("Surgical Department", "1234567893")
        ]
        for d in depts:
            self.department_dao.add_department(d)
        self.departments = self.department_dao.get_all_departments()

    def _initialize_default_employees(self):
        emps = [
            Employee("D001", "Dr. Rajesh Kumar", 45, "Male", 150000.0, "9876543210", "rajesh.kumar@hospital.com", "Cardiologist"),
            Employee("D002", "Dr. Priya Sharma", 38, "Female", 140000.0, "9876543211", "priya.sharma@hospital.com", "Neurologist"),
            Employee("D003", "Dr. Amit Patel", 42, "Male", 145000.0, "9876543212", "amit.patel@hospital.com", "Orthopedic"),
            Employee("D004", "Dr. Sneha Gupta", 35, "Female", 135000.0, "9876543213", "sneha.gupta@hospital.com", "Pediatrician"),
            Employee("D005", "Dr. Vikram Singh", 50, "Male", 130000.0, "9876543214", "vikram.singh@hospital.com", "General Physician"),
            Employee("N001", "Sarah Wilson", 32, "Female", 80000.0, "9876543215", "sarah.wilson@hospital.com", "Head Nurse"),
            Employee("N002", "John Smith", 35, "Male", 75000.0, "9876543216", "john.smith@hospital.com", "Emergency Nurse"),
            Employee("N003", "Maria Garcia", 28, "Female", 70000.0, "9876543217", "maria.garcia@hospital.com", "ICU Nurse"),
            Employee("N004", "David Chen", 30, "Male", 72000.0, "9876543218", "david.chen@hospital.com", "Surgical Nurse"),
            Employee("N005", "Lisa Anderson", 33, "Female", 68000.0, "9876543219", "lisa.anderson@hospital.com", "Pediatric Nurse")
        ]
        for e in emps:
            self.employee_dao.add_employee(e)
        self.employees = self.employee_dao.get_all_employees()

    def _initialize_default_ambulances(self):
        ambs = [
            Ambulance("AMB001", "Harsh Sathe", "9876543210", "MH12AB1234"),
            Ambulance("AMB002", "Shardul Walunj", "9876543211", "MH12CD5678"),
            Ambulance("AMB003", "Savit Pandita", "9876543212", "MH12EF9012", is_available=False),
            Ambulance("AMB004", "Shrikar Bende", "9876543213", "MH12GH3456"),
            Ambulance("AMB005", "Rajshekhar Shinde", "9876543214", "MH12IJ7890")
        ]
        for a in ambs:
            self.ambulance_dao.add_ambulance(a)
        self.ambulances = self.ambulance_dao.get_all_ambulances()

    def _initialize_default_rooms(self):
        rooms = []
        for i in range(1, 11): rooms.append(Room(f"S{i}", "Single", 1500.0, True))
        for i in range(1, 11): rooms.append(Room(f"D{i}", "Double", 2500.0, True))
        for i in range(1, 6): rooms.append(Room(f"SU{i}", "Suite", 5000.0, True))
        for i in range(1, 6): rooms.append(Room(f"ICU{i}", "ICU", 8000.0, True))
        for i in range(1, 4): rooms.append(Room(f"DL{i}", "Deluxe", 3500.0, True))
        for i in range(1, 16): rooms.append(Room(f"GW{i}", "General Ward", 800.0, True))
        for i in range(1, 9): rooms.append(Room(f"P{i}", "Pediatric", 2000.0, True))
        for i in range(1, 7): rooms.append(Room(f"M{i}", "Maternity", 3000.0, True))
        for r in rooms:
            self.room_dao.add_room(r)
        self.rooms = self.room_dao.get_all_rooms()

    def login(self, username: str, password: str) -> bool:
        return (username is not None and password is not None and
                username.strip() == self.DEFAULT_USERNAME and
                password.strip() == self.DEFAULT_PASSWORD)

    # Patient Management
    def add_patient(self, patient: Patient) -> bool:
        if not self.validate_patient(patient):
            print("Patient validation failed!")
            return False
        added = self.patient_dao.add_patient(patient)
        if added:
            if patient.room_number:
                room = self.find_room_by_number(patient.room_number)
                if room:
                    room.available = False
                    self.update_room(room)
            self.patients = self.get_all_patients()
            return True
        print("Patient NOT added to database!")
        return False

    def get_all_patients(self) -> List[Patient]:
        return self.patient_dao.get_all_patients()

    def find_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        return self.patient_dao.get_patient_by_id(patient_id)

    def update_patient(self, patient: Patient) -> bool:
        updated = self.patient_dao.update_patient(patient)
        if updated:
            self.patients = self.get_all_patients()
        return updated

    def discharge_patient(self, patient_id: str, amount_paid: float) -> bool:
        patient = self.find_patient_by_id(patient_id)
        if not patient:
            return False

        patient.amount_paid += amount_paid
        patient.pending_amount = max(0.0, patient.pending_amount - amount_paid)
        patient.discharge_date = datetime.now()

        if patient.room_number:
            room = self.find_room_by_number(patient.room_number)
            if room:
                room.available = True
                self.room_dao.update_room(room)

        return self.patient_dao.update_patient(patient)

    # Room Management
    def get_all_rooms(self) -> List[Room]:
        return self.room_dao.get_all_rooms()

    def get_available_rooms(self) -> List[Room]:
        return [r for r in self.get_all_rooms() if r.available]

    def get_rooms_by_bed_type(self, bed_type: str) -> List[Room]:
        return [r for r in self.get_all_rooms() if r.bed_type.lower() == bed_type.lower()]

    def find_room_by_number(self, room_number: str) -> Optional[Room]:
        return self.room_dao.get_room_by_number(room_number)

    def update_room(self, room: Room) -> bool:
        return self.room_dao.update_room(room)

    def add_room(self, room: Room) -> bool:
        return self.room_dao.add_room(room)

    def delete_room(self, room_number: str) -> bool:
        return self.room_dao.delete_room(room_number)

    # Department Management
    def get_all_departments(self) -> List[Department]:
        return self.department_dao.get_all_departments()

    def add_department(self, department: Department) -> bool:
        return self.department_dao.add_department(department)

    # Employee Management
    def get_all_employees(self) -> List[Employee]:
        return self.employee_dao.get_all_employees()

    def add_employee(self, employee: Employee) -> bool:
        return self.employee_dao.add_employee(employee)

    # Ambulance Management
    def get_all_ambulances(self) -> List[Ambulance]:
        return self.ambulance_dao.get_all_ambulances()

    def get_available_ambulances(self) -> List[Ambulance]:
        return [a for a in self.get_all_ambulances() if a.is_available]

    def book_ambulance(self, ambulance_id: str) -> bool:
        for a in self.get_all_ambulances():
            if a.ambulance_id.lower() == ambulance_id.lower() and a.is_available:
                return self.ambulance_dao.update_availability(a.ambulance_id, False)
        return False

    def release_ambulance(self, ambulance_id: str) -> bool:
        return self.ambulance_dao.update_availability(ambulance_id, True)

    def export_patients_to_csv(self, file_path: str):
        try:
            with open(file_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Gender", "Disease", "Admission Date", "Room Number"])
                for p in self.get_all_patients():
                    writer.writerow([
                        p.patient_id, p.name, p.gender, p.disease,
                        p.admission_time.isoformat(), p.room_number or "N/A"
                    ])
            print(f"Exported patients to {file_path}")
        except Exception as e:
            print(f"Error exporting patients to CSV: {e}")

    def backup_database(self, backup_path: str):
        try:
            os.makedirs(backup_path, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_path, f"hospital_db_backup_{timestamp}.sql")
            
            cmd = ["mysqldump", "-u", "root", "-p431001", "hospital_db"]
            with open(backup_file, "w") as out:
                subprocess.run(cmd, stdout=out, check=True)
            print(f"Database backup created at {backup_file}")
        except Exception as e:
            print(f"Error creating database backup: {e}")

    def validate_patient(self, patient: Patient) -> bool:
        if not patient:
            print("Patient cannot be None")
            return False
        if not patient.patient_id or not patient.patient_id.strip():
            print("Patient ID cannot be empty")
            return False
        if not patient.name or not patient.name.strip():
            print("Patient Name cannot be empty")
            return False
        if patient.deposit_amount < 0:
            print("Deposit amount cannot be negative")
            return False

        if patient.room_number and patient.room_number.strip():
            room = self.find_room_by_number(patient.room_number)
            if not room:
                print(f"Invalid room number: {patient.room_number}")
                return False
            existing_owner = self.find_patient_by_id(patient.patient_id)
            is_self_owned = (existing_owner is not None and
                             existing_owner.room_number and
                             patient.room_number.lower() == existing_owner.room_number.lower())
            if not room.available and not is_self_owned:
                print(f"Room is not available: {patient.room_number}")
                return False

        return True
