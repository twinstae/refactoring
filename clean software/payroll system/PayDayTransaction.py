from PayrollDB import PayrollDB as DB
from Tranaction import Transaction


class PayDayTransaction(Transaction):
    def __init__(self, date):
        self.date = date
        self.pay_check = {}

    def execute(self):
        pay_employee_list = DB.get_all_employees_with_pay_day(self.date)
        for e in pay_employee_list:
            pc = PayCheck(self.date)
            self.pay_check[e.emp_id] = pc
            e.pay_day(pc)

    def get_pay_check(self, emp_id):
        return self.pay_check.get(emp_id, None)


class PayCheck:
    def __init__(self, date):
        self.pay_date = date
        self.gross_pay = None
        self.disposition = None
        self.deductions = 0
        self.net_pay = None
