from Employee import Employee, PaymentClassification, SalariedClassification, HourlyClassification, \
    CommissionedClassification
from abc import *

from PaymentMethod import HoldMethod
from PaymentSchedule import PaymentSchedule, MonthlySchedule, WeeklySchedule, BiweeklySchedule
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
        pass

    def get_employee(self):
        e = Employee(emp_id=self.args['emp_id'],
                     name=self.args['name'],
                     address=self.args['address'])
        e.classification = self.get_classification()
        e.schedule = self.get_schedule()
        e.method = HoldMethod()
        return e

    @staticmethod
    def get_classification():
        pass

    @staticmethod
    def get_schedule():
        pass


class AddHourlyEmployee(AddEmployeeTransaction):
    def execute(self):
        e = self.get_employee()
        e.hourly_rate = self.args['hourly_rate']
        DB.add_employee(DB, self.args['emp_id'], e)

    def get_classification(self):
        return HourlyClassification(self.args['hourly_rate'])

    @staticmethod
    def get_schedule():
        return WeeklySchedule()


class AddSalariedEmployee(AddEmployeeTransaction):
    def execute(self):
        e = self.get_employee()
        e.salary = self.args['salary']
        DB.add_employee(DB, self.args['emp_id'], e)

    def get_classification(self):
        return SalariedClassification(self.args['salary'])

    def get_schedule(self):
        return MonthlySchedule()


class AddCommissionedEmployee(AddEmployeeTransaction):
    def execute(self):
        e = self.get_employee()
        e.salary = self.args['salary']
        e.commission_rate = self.args['commission_rate']
        DB.add_employee(DB, self.args['emp_id'], e)

    def get_classification(self):
        return CommissionedClassification(
            salary=self.args['salary'],
            commission_rate=self.args['commission_rate']
        )

    def get_schedule(self):
        return BiweeklySchedule()


def no_employee():
    msg = "id 없음 : 해당하는 employee가 DB에 없습니다."
    print(msg)
    return msg


class DeleteEmployee(Transaction):

    def __init__(self, emp_id):
        self.emp_id = emp_id

    def execute(self):
        if self.emp_id in DB.its_employee:
            DB.delete_employee(DB, self.emp_id)
        else:
            return no_employee()


class TimeCardTransaction(Transaction):

    def __init__(self, emp_id, date, hours):
        self.emp_id = emp_id
        self.date = date
        self.hours = hours

    def execute(self):
        employee = DB.get_employee(DB, self.emp_id)
        if employee:
            hc = employee.classification
            if isinstance(hc, HourlyClassification):

                time_card = TimeCard(
                    date=self.date,
                    hours=self.hours
                )

                hc.add_time_card(time_card)
            else:
                msg = "she/he is not a hourly employee"
                print(msg)
                return msg
        else:
            return no_employee()


class SalesReceiptTransaction(Transaction):
    def __init__(self, emp_id, date, amount):
        self.emp_id = emp_id
        self.date = date
        self.amount = amount

    def execute(self):
        employee = DB.get_employee(DB, self.emp_id)
        if employee:
            cc = employee.classification
            if isinstance(cc, CommissionedClassification):
                cc.add_sales(
                    sales=SalesReceipt(
                        date=self.date,
                        amount=self.amount
                    )
                )
            else:
                msg = "she/he is not a commissioned employee"
                print(msg)
                return msg
        else:
            return no_employee()