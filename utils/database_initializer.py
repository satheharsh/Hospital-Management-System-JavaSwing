import os
from utils.database_util import DatabaseUtil

class DatabaseInitializer:

    @staticmethod
    def initialize_database() -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()

            sql_statements = [
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    room_number VARCHAR(10) PRIMARY KEY,
                    bed_type VARCHAR(20) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    available BOOLEAN DEFAULT TRUE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS patients (
                    id VARCHAR(10) PRIMARY KEY,
                    id_type VARCHAR(20) NOT NULL,
                    id_number VARCHAR(50) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    disease VARCHAR(200) NOT NULL,
                    admission_time DATETIME NOT NULL,
                    deposit_amount DECIMAL(10, 2) NOT NULL,
                    room_number VARCHAR(10),
                    pending_amount DECIMAL(10, 2) NOT NULL,
                    amount_paid DECIMAL(10, 2) NOT NULL,
                    discharge_date DATETIME,
                    FOREIGN KEY (room_number) REFERENCES rooms(room_number)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    salary DECIMAL(10, 2) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    role VARCHAR(50) NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS ambulances (
                    ambulance_id VARCHAR(10) PRIMARY KEY,
                    driver_name VARCHAR(100) NOT NULL,
                    driver_phone VARCHAR(20) NOT NULL,
                    plate_number VARCHAR(20) NOT NULL,
                    is_available BOOLEAN DEFAULT TRUE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS departments (
                    name VARCHAR(50) PRIMARY KEY,
                    phone_number VARCHAR(20) NOT NULL
                );
                """
            ]

            for statement in sql_statements:
                cursor.execute(statement)

            conn.commit()
            cursor.close()
            conn.close()
            print("Database initialized successfully.")
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
