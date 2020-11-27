from Employee import Employee, PaymentClassification, SalariedClassification, HourlyClassification
from abc import *

from PaymentMethod import HoldMethod
from PaymentSchedule import PaymentSchedule, MonthlySchedule, WeeklySchedule
from PayrollDB import PayrollDB as DB


class Transaction(metaclass=ABCMeta):

    @abstractmethod
    def execute(self):
        pass


class AddEmployeeTransaction(Transaction):
    def __init__(self, emp_id, name, address):
        self.emp_id = emp_id
        self.name = name
        self.address = address

    def execute(self):
        pass

    @staticmethod
    def get_classification():
        pass

    @staticmethod
    def get_schedule():
        pass


class AddSalariedEmployee(AddEmployeeTransaction):
    def __init__(self, emp_id, name, address, salary):
        super().__init__(emp_id, name, address)
        self.salary = salary

    def execute(self):
        e = Employee(self.emp_id, self.name, self.address)
        e.classification = self.get_classification()
        e.schedule = self.get_schedule()
        e.method = HoldMethod()
        e.salary = self.salary

        DB.add_employee(DB, self.emp_id, e)

    @staticmethod
    def get_classification():
        return SalariedClassification()

    @staticmethod
    def get_schedule():
        return MonthlySchedule()


class AddHourlyEmployee(AddEmployeeTransaction):
    def __init__(self, emp_id, name, address, hourly_rate):
        super().__init__(emp_id, name, address)
        self.hourly_rate = hourly_rate

    def execute(self):
        e = Employee(self.emp_id, self.name, self.address)
        e.classification = self.get_classification()
        e.schedule = self.get_schedule()
        e.method = HoldMethod()
        e.hourly_rate = self.hourly_rate

        DB.add_employee(DB, self.emp_id, e)

    @staticmethod
    def get_classification():
        return HourlyClassification()

    @staticmethod
    def get_schedule():
        return WeeklySchedule()
