from datetime import datetime
from typing import List, Optional
from models.patient import Patient
from utils.database_util import DatabaseUtil

class PatientDAO:

    def _row_to_patient(self, row) -> Patient:
        if isinstance(row, dict):
            p_id = row['id']
            id_type = row['id_type']
            id_num = row['id_number']
            name = row['name']
            gender = row['gender']
            disease = row['disease']
            adm_time = row['admission_time']
            dep_amt = row['deposit_amount']
            rm_num = row['room_number']
            pend_amt = row['pending_amount']
            amt_pd = row['amount_paid']
            dis_date = row['discharge_date']
        else:
            p_id, id_type, id_num, name, gender, disease, adm_time, dep_amt, rm_num, pend_amt, amt_pd, dis_date = row[:12]

        if isinstance(adm_time, str):
            adm_time = datetime.fromisoformat(adm_time)
        if dis_date and isinstance(dis_date, str):
            dis_date = datetime.fromisoformat(dis_date)

        patient = Patient(p_id, id_type, id_num, name, gender, disease, adm_time, float(dep_amt))
        patient.room_number = rm_num
        patient.pending_amount = float(pend_amt)
        patient.amount_paid = float(amt_pd)
        patient.discharge_date = dis_date
        return patient

    def get_all_patients(self) -> List[Patient]:
        patients = []
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "SELECT id, id_type, id_number, name, gender, disease, admission_time, deposit_amount, room_number, pending_amount, amount_paid, discharge_date FROM patients")
            rows = cursor.fetchall()
            for row in rows:
                patients.append(self._row_to_patient(row))
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error getting patients: {e}")
        return patients

    def get_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "SELECT id, id_type, id_number, name, gender, disease, admission_time, deposit_amount, room_number, pending_amount, amount_paid, discharge_date FROM patients WHERE id = %s", (patient_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                return self._row_to_patient(row)
        except Exception as e:
            print(f"Error getting patient by id: {e}")
        return None

    def add_patient(self, patient: Patient) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "INSERT INTO patients (id, id_type, id_number, name, gender, disease, admission_time, deposit_amount, room_number, pending_amount, amount_paid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                patient.patient_id, patient.id_type, patient.id_number, patient.name,
                patient.gender, patient.disease, patient.admission_time.isoformat(),
                patient.deposit_amount, patient.room_number, patient.pending_amount, patient.amount_paid
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding patient: {e}")
            return False

    def update_patient(self, patient: Patient) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            dis_date_str = patient.discharge_date.isoformat() if patient.discharge_date else None
            DatabaseUtil.execute(cursor, "UPDATE patients SET id_type = %s, id_number = %s, name = %s, gender = %s, disease = %s, admission_time = %s, deposit_amount = %s, room_number = %s, pending_amount = %s, amount_paid = %s, discharge_date = %s WHERE id = %s", (
                patient.id_type, patient.id_number, patient.name, patient.gender,
                patient.disease, patient.admission_time.isoformat(), patient.deposit_amount,
                patient.room_number, patient.pending_amount, patient.amount_paid,
                dis_date_str, patient.patient_id
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating patient: {e}")
            return False

    def delete_patient(self, patient_id: str) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "DELETE FROM patients WHERE id = %s", (patient_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False
