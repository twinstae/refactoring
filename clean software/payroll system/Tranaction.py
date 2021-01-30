from Employee import Employee, SalariedClassification, HourlyClassification, \
    CommissionedClassification
from abc import *

from PaymentMethod import pay_hold
from PaymentSchedule import is_weekly_friday, is_monthly_friday, is_biweekly_pay_day
from PayrollDB import PayrollDB as DB
from SalesReceipt import SalesReceipt
from TimeCard import TimeCard


class Transaction(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


def add_employee_transaction(arg_dict, classification, schedule):
    def execute():
        if 'emp_id' not in arg_dict:
            raise NoEmpIdError

        e = Employee(
            arg_dict=arg_dict,
            classification=classification,
            schedule=schedule,
            method=pay_hold
        )
        DB.add_employee(e.emp_id, e)
        return e

    return execute


class NoEmpIdError(Exception):
    def __str__(self):
        return "arg에 emp_id가 없습니다"


def add_hourly_employee_transaction(arg_dict):
    if 'hourly_rate' not in arg_dict:
        raise NoHourlyError

    return add_employee_transaction(
        arg_dict,
        classification=HourlyClassification(arg_dict['hourly_rate']),
        schedule=is_weekly_friday
    )


class NoHourlyError(Exception):
    def __str__(self):
        return "arg에 hourly_rate가 없습니다"


def add_salaried_employee_transaction(arg_dict):
    if 'salary' not in arg_dict:
        raise NoSalaryError

    return add_employee_transaction(
        arg_dict,
        classification=SalariedClassification(arg_dict['salary']),
        schedule=is_monthly_friday
    )


class NoSalaryError(Exception):
    def __str__(self):
        return "arg에 salary가 없습니다"


def add_commissioned_employee_transaction(arg_dict):
    if 'salary' not in arg_dict:
        raise NoSalaryError

    if 'commission_rate' not in arg_dict:
        raise NoCommissionError

    return add_employee_transaction(
        arg_dict,
        classification=CommissionedClassification(
            salary=arg_dict['salary'],
            commission_rate=arg_dict['commission_rate']
        ),
        schedule=is_biweekly_pay_day
    )


class NoCommissionError(Exception):
    def __str__(self):
        return "arg에 commission_rate가 없습니다"


class DeleteEmployee(Transaction):
    def __init__(self, emp_id):
        self.emp_id = emp_id

    def execute(self):
        DB.delete_employee(self.emp_id)


class TimeCardTransaction(Transaction):
    def __init__(self, emp_id, date, hours):
        self.emp_id = emp_id
        self.date = date
        self.hours = hours

    def execute(self):
        employee = DB.get_employee(self.emp_id)

        hc = employee.classification
        if isinstance(hc, HourlyClassification):

            time_card = TimeCard(
                date=self.date,
                hours=self.hours
            )

            hc.add_time_card(time_card)
        else:
            raise NotHourlyError


class NotHourlyError(Exception):
    def __str__(self):
        return "hourly employee가 아닙니다."


class SalesReceiptTransaction(Transaction):
    def __init__(self, emp_id, date, amount):
        self.emp_id = emp_id
        self.date = date
        self.amount = amount

    def execute(self):
        employee = DB.get_employee(self.emp_id)

        cc = employee.classification
        if isinstance(cc, CommissionedClassification):
            cc.add_sales(
                sales=SalesReceipt(
                    date=self.date,
                    amount=self.amount
                )
            )
        else:
            raise NotCommissionedError


class NotCommissionedError(Exception):
    def __str__(self):
        return "commissioned employee가 아닙니다."
