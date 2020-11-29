import unittest

from datetime import date

from Employee import SalariedClassification
from PayDayTransaction import PayDayTransaction
from PaymentSchedule import MonthlySchedule
from PayrollDB import PayrollDB as DB
from Tranaction import AddSalariedEmployee


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
        self.arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
        }
        t = AddSalariedEmployee(self.arg_dict)
        t.execute()
        self.employee = self.validate_get_employee(self.arg_dict)

        self.hc = self.employee.classification
        self.assertIsInstance(self.hc, SalariedClassification)

    def tearDown(self) -> None:
        DB.clear()

    def test_monthly_schedule(self):
        pay_date = date(2001, 11, 30)
        ms = MonthlySchedule()
        self.assertTrue(ms.is_pay_day(pay_date))

    def test_employee_is_pay_day(self):
        pay_date = date(2001, 11, 30)
        self.assertIsInstance(
            self.employee.schedule, MonthlySchedule
        )
        self.assertTrue(
            self.employee.schedule.is_pay_day(pay_date)
        )
        self.assertTrue(
            self.employee.is_pay_day(pay_date)
        )

    def test_get_all_employees_with_pay_day(self):
        pay_date = date(2001, 11, 30)
        e_list = DB.get_all_employees_with_pay_day(pay_date)
        self.assertEqual(1, len(e_list))

    def test_pay_single_salaried(self):
        pay_date = date(2001, 11, 30)
        t = PayDayTransaction(pay_date)
        t.execute()
        pc = t.get_pay_check(self.employee.emp_id)
        self.assertIsNotNone(pc)
        self.assertEqual(pc.pay_date, pay_date)
        self.assertEqual(pc.gross_pay, self.arg_dict['salary'])
        self.assertEqual(pc.deductions, 0)
        self.assertEqual(pc.net_pay, self.arg_dict['salary'])
        self.assertEqual(pc.disposition, "Hold")

    def test_pay_single_salaried_on_wrong_date(self):
        pay_date = date(2001, 11, 29)
        t = PayDayTransaction(pay_date)
        t.execute()
        pc = t.get_pay_check(self.employee.emp_id)
        self.assertIsNone(pc)


if __name__ == '__main__':
    unittest.main()
