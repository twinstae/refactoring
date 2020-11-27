from Employee import Employee, PaymentClassification, SalariedClassification, HourlyClassification, \
    CommissionedClassification
from abc import *

from PaymentMethod import HoldMethod
from PaymentSchedule import PaymentSchedule, MonthlySchedule, WeeklySchedule, BiweeklySchedule
from PayrollDB import PayrollDB as DB


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
