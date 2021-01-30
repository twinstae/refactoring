from PayrollDB import PayrollDB as DB


def pay_day_transaction(date):
    def execute():
        pay_check = {}
        pay_employee_list = DB.get_all_employees_with_pay_day(date)
        for e in pay_employee_list:
            pc = PayCheck(date)
            pay_check[e.emp_id] = pc
            e.pay_day(pc)

        return pay_check
    return execute


class PayCheck:
    def __init__(self, date):
        self.pay_date = date
        self.gross_pay = None
        self.disposition = None
        self.deductions = 0
        self.net_pay = None
