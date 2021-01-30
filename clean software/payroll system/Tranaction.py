from Employee import Employee, PaymentClassification, SalariedClassification, HourlyClassification, \
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


class AddEmployeeTransaction(Transaction):
    def __init__(self, arg_dict):
        self.args = arg_dict

    def execute(self):
        if 'emp_id' not in self.args:
            raise NoEmpIdError

        e = self.get_employee()
        DB.add_employee(self.args['emp_id'], e)
        return e

    def get_employee(self):
        cls = self.get_classification()

        e = Employee(
            arg_dict=self.args,
            classification=cls,
            schedule=self.get_schedule(),
            method=pay_hold
        )
        return e

    @staticmethod
    def get_classification():
        pass

    @staticmethod
    def get_schedule():
        pass


class NoEmpIdError(Exception):
    def __str__(self):
        return "arg에 emp_id가 없습니다"


class AddHourlyEmployee(AddEmployeeTransaction):
    def get_classification(self):
        if 'hourly_rate' not in self.args:
            raise NoHourlyError
        return HourlyClassification(self.args['hourly_rate'])

    @staticmethod
    def get_schedule():
        return is_weekly_friday


class NoHourlyError(Exception):
    def __str__(self):
        return "arg에 hourly_rate가 없습니다"


class AddSalariedEmployee(AddEmployeeTransaction):
    def get_classification(self):
        if 'salary' not in self.args:
            raise NoSalaryError
        return SalariedClassification(self.args['salary'])

    def get_schedule(self):
        return is_monthly_friday


class NoSalaryError(Exception):
    def __str__(self):
        return "arg에 salary가 없습니다"


class AddCommissionedEmployee(AddEmployeeTransaction):
    def get_classification(self):

        if 'salary' not in self.args:
            raise NoSalaryError

        if 'commission_rate' not in self.args:
            raise NoCommissionError

        return CommissionedClassification(
            salary=self.args['salary'],
            commission_rate=self.args['commission_rate']
        )

    def get_schedule(self):
        return is_biweekly_pay_day


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
