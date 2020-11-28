from Employee import PaymentClassification, SalariedClassification, HourlyClassification, CommissionedClassification
from Tranaction import Transaction
from PayrollDB import PayrollDB as DB


class ChangeEmployeeTransaction(Transaction):
    def __init__(self, emp_id):
        the_employee = DB.get_employee(DB, emp_id)
        self.employee = the_employee

    def execute(self):
        self.change_attr()
        DB.change_employee(
            DB,
            emp_id=self.employee.emp_id,
            new_employee=self.employee
        )

    def change_attr(self):
        pass


class ChangeNameTransaction(ChangeEmployeeTransaction):
    def __init__(self, emp_id, new_name):
        super().__init__(emp_id)
        self.new_name = new_name

    def change_attr(self):
        self.employee.name = self.new_name


class ChangeAddressTransaction(ChangeEmployeeTransaction):
    def __init__(self, emp_id, new_address):
        super().__init__(emp_id)
        self.new_address = new_address

    def change_attr(self):
        self.employee.address = self.new_address


class ChangeClassificationTransaction(ChangeEmployeeTransaction):
    def change_attr(self):
        self.employee.classification = self.get_classification()

    def get_classification(self):
        return PaymentClassification()


class ChangeHourlyTransaction(ChangeClassificationTransaction):
    def __init__(self, emp_id, hourly_rate):
        super().__init__(emp_id)
        self.employee.hourly_rate = hourly_rate

    def get_classification(self):
        return HourlyClassification(self.employee.hourly_rate)


class ChangeSalariedTransaction(ChangeClassificationTransaction):
    def __init__(self, emp_id, salary):
        super().__init__(emp_id)
        self.employee.salary = salary

    def get_classification(self):
        return SalariedClassification(
            salary=self.employee.salary
        )


class ChangeCommissionedTransaction(ChangeClassificationTransaction):
    def __init__(self, emp_id, salary, commission_rate):
        super().__init__(emp_id)
        self.employee.salary = salary
        self.employee.commission_rate = commission_rate

    def get_classification(self):
        return CommissionedClassification(
            salary=self.employee.salary,
            commission_rate=self.employee.commission_rate
        )
