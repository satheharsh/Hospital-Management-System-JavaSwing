from typing import List
from models.department import Department
from utils.database_util import DatabaseUtil

class DepartmentDAO:

    def get_all_departments(self) -> List[Department]:
        departments = []
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "SELECT name, phone_number FROM departments")
            rows = cursor.fetchall()
            for row in rows:
                if isinstance(row, dict):
                    name, phone = row['name'], row['phone_number']
                else:
                    name, phone = row[0], row[1]
                departments.append(Department(name, phone))
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error getting departments: {e}")
        return departments

    def add_department(self, dept: Department) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "INSERT INTO departments (name, phone_number) VALUES (%s, %s)", (dept.name, dept.phone_number))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding department: {e}")
            return False
