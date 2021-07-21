import unittest

from datetime import date

from PayDayTransaction import pay_day_transaction
from PaymentSchedule import is_monthly_friday
from PayrollDB import PayrollDB as DB
from Tranaction import add_salaried_employee_transaction, \
    add_hourly_employee_transaction, add_commissioned_employee_transaction, add_time_card_transaction, \
    add_sales_receipt_transaction


class TestPay(unittest.TestCase):
    def new_employee(self, arg_dict, add_employee):
        t = add_employee(arg_dict)
        t.execute()
        employee = DB.get_employee(arg_dict['emp_id'])
        for attr_name, attr_value in arg_dict.items():
            self.assertTrue(getattr(employee, attr_name) == attr_value)
        return employee

    def validate_get_employee(self, arg_dict):
        employee = DB.get_employee(arg_dict['emp_id'])
        for attr_name, attr_value in arg_dict.items():
            self.assertTrue(getattr(employee, attr_name) == attr_value)
        return employee

    def setUp(self) -> None:
        self.salaried_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
        }
        transaction = add_salaried_employee_transaction(self.salaried_dict)
        transaction()
        self.salaried_employee = self.validate_get_employee(self.salaried_dict)

        self.hourly_dict = {
            'emp_id': 2,
            'name': "김재희",
            'address': "파주",
            'hourly_rate': 10.0
        }
        transaction2 = add_hourly_employee_transaction(self.hourly_dict)
        transaction2()

        self.commissioned_dict = {
            'emp_id': 3,
            'name': "김희선",
            'address': "서울",
            'salary': 1000.0,
            'commission_rate': 0.1
        }
        transaction3 = add_commissioned_employee_transaction(self.commissioned_dict)
        transaction3()

    def tearDown(self) -> None:
        DB.clear()

    def test_monthly_schedule(self):
        pay_date = date(2001, 11, 30)
        self.assertTrue(is_monthly_friday(pay_date))

    def test_get_weekly_employees_with_pay_day(self):
        pay_date = date(2020, 11, 20)
        e_list = DB.get_all_employees_with_pay_day(pay_date)
        self.assertEqual(1, len(e_list))  # hourly

    def test_get_bi_and_weekly_employees_with_pay_day(self):
        pay_date = date(2020, 11, 27)
        e_list = DB.get_all_employees_with_pay_day(pay_date)
        self.assertEqual(2, len(e_list))  # hourly, commissioned

    def test_get_monthly_employees_with_pay_day(self):
        pay_date = date(2020, 11, 30)
        e_list = DB.get_all_employees_with_pay_day(pay_date)
        self.assertEqual(1, len(e_list))  # monthly

    def test_pay_single_salaried(self):
        pay_date = date(2001, 11, 30)
        pc = self.pay_check(pay_date, self.salaried_employee.emp_id)
        self.check_pc(self.salaried_dict['salary'], pay_date, pc)

    def test_pay_single_salaried_on_wrong_date(self):
        pay_date = date(2001, 11, 29)
        pc = self.pay_check(pay_date, self.salaried_employee.emp_id)
        self.assertIsNone(pc)

    def add_time_card(self):
        transaction = add_time_card_transaction(
            emp_id=self.hourly_dict['emp_id'],
            date=date(2020, 11, 21),
            hours=10.0
        )
        transaction()

    def pay_hourly(self, pay_date, hours):
        self.add_time_card()
        pc = self.pay_check(pay_date, self.hourly_dict['emp_id'])
        gross_pay = self.hourly_dict['hourly_rate'] * hours  # 0시간 일함
        self.check_pc(gross_pay, pay_date, pc)

    def test_pay_single_hourly_before(self):
        self.pay_hourly(
            pay_date=date(2020, 11, 20),
            hours=0
        )

    def test_pay_single_hourly(self):
        self.pay_hourly(
            pay_date=date(2020, 11, 27),  # 금요일
            hours=10
        )

    def test_pay_single_hourly_after(self):
        self.pay_hourly(
            pay_date=date(2020, 12, 4),
            hours=0
        )

    def add_sales(self):
        transaction = add_sales_receipt_transaction(
            emp_id=self.commissioned_dict['emp_id'],
            date=date(2020, 11, 14),  # 경계값
            amount=1000
        )
        transaction()

    def test_pay_single_commissioned(self):
        self.add_sales()
        pay_date = date(2020, 11, 27)  # 2주마다 돌아오는 금요일
        c_dict = self.commissioned_dict
        pc = self.pay_check(pay_date, c_dict['emp_id'])
        gross_pay = c_dict['salary'] + c_dict['commission_rate'] * 1000  # 1000 매출
        self.check_pc(gross_pay, pay_date, pc)

    @staticmethod
    def pay_check(pay_date, emp_id):
        transaction = pay_day_transaction(pay_date)
        pay_check = transaction()
        return pay_check.get(emp_id, None)

    def check_pc(self, gross_pay, pay_date, pc):
        self.assertIsNotNone(pc)
        self.assertEqual(pay_date, pc.pay_date)
        self.assertEqual(gross_pay, pc.gross_pay)
        self.assertEqual(0, pc.deductions)
        self.assertEqual(gross_pay, pc.net_pay)
        self.assertEqual("Hold", pc.disposition)


if __name__ == '__main__':
    unittest.main()
