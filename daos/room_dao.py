from typing import List, Optional
from models.room import Room
from utils.database_util import DatabaseUtil

class RoomDAO:

    def get_all_rooms(self) -> List[Room]:
        rooms = []
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "SELECT room_number, bed_type, price, available FROM rooms")
            rows = cursor.fetchall()
            for row in rows:
                if isinstance(row, dict):
                    r_num, b_type, pr, av = row['room_number'], row['bed_type'], row['price'], row['available']
                else:
                    r_num, b_type, pr, av = row[0], row[1], row[2], row[3]
                rooms.append(Room(r_num, b_type, float(pr), bool(av)))
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error getting rooms: {e}")
        return rooms

    def get_room_by_number(self, room_number: str) -> Optional[Room]:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "SELECT room_number, bed_type, price, available FROM rooms WHERE room_number = %s", (room_number,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                if isinstance(row, dict):
                    r_num, b_type, pr, av = row['room_number'], row['bed_type'], row['price'], row['available']
                else:
                    r_num, b_type, pr, av = row[0], row[1], row[2], row[3]
                return Room(r_num, b_type, float(pr), bool(av))
        except Exception as e:
            print(f"Error getting room by number: {e}")
        return None

    def add_room(self, room: Room) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "INSERT INTO rooms (room_number, bed_type, price, available) VALUES (%s, %s, %s, %s)", (room.room_number, room.bed_type, room.price, room.available))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding room: {e}")
            return False

    def update_room(self, room: Room) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "UPDATE rooms SET bed_type = %s, price = %s, available = %s WHERE room_number = %s", (room.bed_type, room.price, room.available, room.room_number))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating room: {e}")
            return False

    def delete_room(self, room_number: str) -> bool:
        try:
            conn = DatabaseUtil.get_connection()
            cursor = conn.cursor()
            DatabaseUtil.execute(cursor, "DELETE FROM rooms WHERE room_number = %s", (room_number,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting room: {e}")
            return False
