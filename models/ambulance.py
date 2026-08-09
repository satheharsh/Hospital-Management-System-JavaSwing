class Ambulance:
    def __init__(self, ambulance_id: str, driver_name: str, driver_phone: str, plate_number: str, is_available: bool = True):
        self.ambulance_id = ambulance_id
        self.driver_name = driver_name
        self.driver_phone = driver_phone
        self.plate_number = plate_number
        self.is_available = is_available

    def __repr__(self):
        return f"Ambulance(id='{self.ambulance_id}', driver='{self.driver_name}', available={self.is_available})"
