import sqlite3
from typing import List
from models.employee import Employee
from utils.database_util import DatabaseUtil

class EmployeeDAO:

    def get_all_employees(self) -> List[Employee]:
        employees = []
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "SELECT employee_id, name, age, gender, salary, phone_number, email, role FROM employees")
            rows = cursor.fetchall()
            for row in rows:
                if isinstance(row, (dict, sqlite3.Row)):
                    emp_id, name, age, gender, salary, phone, email, role = (
                        row['employee_id'], row['name'], row['age'], row['gender'],
                        row['salary'], row['phone_number'], row['email'], row['role']
                    )
                else:
                    emp_id, name, age, gender, salary, phone, email, role = row[:8]
                employees.append(Employee(emp_id, name, int(age), gender, float(salary), phone, email, role))
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error getting employees: {e}")
        return employees

    def add_employee(self, emp: Employee) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "INSERT INTO employees (employee_id, name, age, gender, salary, phone_number, email, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (emp.employee_id, emp.name, emp.age, emp.gender, emp.salary, emp.phone_number, emp.email, emp.role))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding employee: {e}")
            return False
