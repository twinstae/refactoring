class Employee:
    def __init__(self, name, emp_id, address):
        self.name = name
        self.emp_id = emp_id
        self.address = address


class HourlyEmployee(Employee):


class CommissionedEmployee(Employee):


class SalariedEmployee(Employee):