class Employee:
    def __init__(self, employee_id: str, name: str, age: int, gender: str,
                 salary: float, phone_number: str, email: str, role: str):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.gender = gender
        self.salary = salary
        self.phone_number = phone_number
        self.email = email
        self.role = role

    def __repr__(self):
        return f"Employee(id='{self.employee_id}', name='{self.name}', role='{self.role}')"
