from Employee import SalariedClassification, HourlyClassification, CommissionedClassification
from PaymentSchedule import is_weekly_friday, is_monthly_friday, is_biweekly_pay_day
from PayrollDB import PayrollDB as DB


def change_employee_transaction(emp_id, get_update_employee):
    def execute():
        employee = DB.get_employee(emp_id)
        DB.change_employee(
            emp_id=emp_id,
            new_employee=get_update_employee(employee)
        )
    return execute


def change_name_transaction(emp_id, new_name):
    def get_update_employee(employee):
        employee.name = new_name
        return employee

    return change_employee_transaction(
        emp_id,
        get_update_employee
    )


def change_address_transaction(emp_id, new_address):
    def get_update_employee(employee):
        employee.address = new_address
        return employee

    return change_employee_transaction(
        emp_id,
        get_update_employee
    )


def change_hourly_transaction(emp_id, hourly_rate):
    def get_update_employee(employee):
        employee.hourly_rate = hourly_rate
        employee.classification = HourlyClassification(hourly_rate)
        employee.schedule = is_weekly_friday
        return employee

    return change_employee_transaction(
        emp_id,
        get_update_employee
    )


def change_salaried_transaction(emp_id, salary):
    def get_update_employee(employee):
        employee.salary = salary
        employee.classification = SalariedClassification(salary)
        employee.schedule = is_monthly_friday
        return employee

    return change_employee_transaction(
        emp_id,
        get_update_employee
    )


def change_commissioned_transaction(emp_id, salary, commission_rate):
    def get_update_employee(employee):
        employee.salary = salary
        employee.commission_rate = commission_rate
        employee.classification = CommissionedClassification(
            salary=salary,
            commission_rate=commission_rate
        )
        employee.schedule = is_biweekly_pay_day
        return employee

    return change_employee_transaction(
        emp_id,
        get_update_employee
    )
