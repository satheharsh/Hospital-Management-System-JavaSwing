class Room:
    def __init__(self, room_number: str, bed_type: str, price: float, available: bool = True):
        self.room_number = room_number
        self.bed_type = bed_type
        self.price = price
        self.available = available

    def __repr__(self):
        return f"Room(number='{self.room_number}', bed_type='{self.bed_type}', price={self.price}, available={self.available})"
