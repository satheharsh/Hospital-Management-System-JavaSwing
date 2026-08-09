from datetime import datetime
from typing import Optional

class Patient:
    def __init__(self, patient_id: str, id_type: str, id_number: str, name: str, gender: str,
                 disease: str, admission_time: datetime, deposit_amount: float):
        self.patient_id = patient_id
        self.id_type = id_type
        self.id_number = id_number
        self.name = name
        self.gender = gender
        self.disease = disease
        self.admission_time = admission_time
        self.deposit_amount = deposit_amount
        self.room_number: Optional[str] = None
        self.pending_amount: float = deposit_amount
        self.amount_paid: float = 0.0
        self.discharge_date: Optional[datetime] = None

    def __repr__(self):
        return f"Patient(id={self.patient_id}, name='{self.name}', room='{self.room_number}')"
