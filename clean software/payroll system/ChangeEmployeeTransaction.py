from Tranaction import Transaction
from PayrollDB import PayrollDB as DB


class ChangeEmployeeTransaction(Transaction):
    def __init__(self, emp_id):
        self.employee = DB.get_employee(DB, emp_id)

    def execute(self):
        pass


class ChangeNameTransaction(ChangeEmployeeTransaction):
    def __init__(self, emp_id, new_name):
        super().__init__(emp_id)
        self.new_name = new_name

    def execute(self):
        self.employee.name = self.new_name
        DB.change_employee(
            DB,
            emp_id=self.employee.emp_id,
            new_employee=self.employee
        )


class ChangeAddressTransaction(ChangeEmployeeTransaction):
    def __init__(self, emp_id, new_address):
        super().__init__(emp_id)
        self.new_address = new_address

    def execute(self):
        self.employee.address = self.new_address
        DB.change_employee(
            DB,
            emp_id=self.employee.emp_id,
            new_employee=self.employee
        )
