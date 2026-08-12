import sqlite3
from typing import List
from models.ambulance import Ambulance
from utils.database_util import DatabaseUtil

class AmbulanceDAO:

    def get_all_ambulances(self) -> List[Ambulance]:
        ambulances = []
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "SELECT ambulance_id, driver_name, driver_phone, plate_number, is_available FROM ambulances")
            rows = cursor.fetchall()
            for row in rows:
                if isinstance(row, (dict, sqlite3.Row)):
                    amb_id, d_name, d_phone, plate, av = (
                        row['ambulance_id'], row['driver_name'], row['driver_phone'],
                        row['plate_number'], row['is_available']
                    )
                else:
                    amb_id, d_name, d_phone, plate, av = row[:5]
                ambulances.append(Ambulance(amb_id, d_name, d_phone, plate, bool(av)))
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error getting ambulances: {e}")
        return ambulances

    def add_ambulance(self, amb: Ambulance) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "INSERT INTO ambulances (ambulance_id, driver_name, driver_phone, plate_number, is_available) VALUES (%s, %s, %s, %s, %s)", (amb.ambulance_id, amb.driver_name, amb.driver_phone, amb.plate_number, amb.is_available))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding ambulance: {e}")
            return False

    def update_availability(self, ambulance_id: str, available: bool) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "UPDATE ambulances SET is_available = %s WHERE ambulance_id = %s", (available, ambulance_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating ambulance availability: {e}")
            return False
