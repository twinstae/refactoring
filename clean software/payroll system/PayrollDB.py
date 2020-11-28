class PayrollDB:
    its_employee = {}
    # key : id
    # value : Employee

    @staticmethod
    def get_employee(cls, emp_id):
        return cls.its_employee.get(emp_id, None)

    @staticmethod
    def add_employee(cls, emp_id, employee):
        cls.its_employee[emp_id] = employee

    @staticmethod
    def change_employee(cls, emp_id, new_employee):
        cls.its_employee[emp_id] = new_employee

    @staticmethod
    def clear(cls):
        cls.its_employee = {}

    @staticmethod
    def delete_employee(cls, emp_id):
        del cls.its_employee[emp_id]
