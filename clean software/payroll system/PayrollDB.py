class PayrollDB:
    its_employee = {}
    # key : id
    # value : Employee

    @staticmethod
    def get_employee(cls, emp_id):
        return cls.its_employee[emp_id]

    @staticmethod
    def add_employee(cls, emp_id, employee):
        cls.its_employee[emp_id] = employee

    @staticmethod
    def clear(cls):
        cls.its_employee = {}
