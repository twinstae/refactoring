from Employee import Employee


class PayrollDB:
    its_employee = {}
    # key : id
    # value : Employee

    @staticmethod
    def get_employee(cls, emp_id):
        PayrollDB.check(cls, emp_id)
        return cls.its_employee[emp_id]

    @staticmethod
    def check(cls, emp_id):
        if emp_id not in cls.its_employee:
            raise NoEmployeeError

    @staticmethod
    def add_employee(cls, emp_id, employee):
        cls.its_employee[emp_id] = employee

    @staticmethod
    def change_employee(cls, emp_id, new_employee):
        PayrollDB.check(cls, emp_id)
        cls.its_employee[emp_id] = new_employee

    @staticmethod
    def clear(cls):
        cls.its_employee = {}

    @staticmethod
    def delete_employee(cls, emp_id):
        PayrollDB.check(cls, emp_id)
        del cls.its_employee[emp_id]


class NoEmployeeError(Exception):
    def __str__(self):
        return "해당하는 id를 가진 employee가 없습니다"
