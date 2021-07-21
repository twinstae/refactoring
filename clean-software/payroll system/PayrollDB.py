from Employee import Employee


class PayrollDB:
    its_employee = {}
    # key : id
    # value : Employee

    @classmethod
    def get_employee(cls, emp_id):
        PayrollDB.check(emp_id)
        return cls.its_employee[emp_id]

    @classmethod
    def check(cls, emp_id):
        if emp_id not in cls.its_employee:
            raise NoEmployeeError

    @classmethod
    def add_employee(cls, emp_id, employee):
        cls.its_employee[emp_id] = employee

    @classmethod
    def change_employee(cls, emp_id, new_employee):
        PayrollDB.check(emp_id)
        cls.its_employee[emp_id] = new_employee

    @classmethod
    def clear(cls):
        cls.its_employee = {}

    @classmethod
    def delete_employee(cls, emp_id):
        PayrollDB.check(emp_id)
        del cls.its_employee[emp_id]

    @classmethod
    def get_all_emp_id(cls):
        return cls.its_employee.keys()

    @classmethod
    def get_all_employees(cls):
        return cls.its_employee.values()

    @classmethod
    def get_all_employees_with_pay_day(cls, date):
        return [e for e in cls.get_all_employees() if e.is_pay_day(date)]


class NoEmployeeError(Exception):
    def __str__(self):
        return "해당하는 id를 가진 employee가 없습니다"
