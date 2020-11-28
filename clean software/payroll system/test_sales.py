import unittest

from Employee import CommissionedClassification, NoSalesError
from PayrollDB import PayrollDB as DB, NoEmployeeError
from SalesReceipt import SalesReceipt
from Tranaction import SalesReceiptTransaction, AddCommissionedEmployee, AddHourlyEmployee, NotCommissionedError


class TestTimeCard(unittest.TestCase):
    def new_employee(self, arg_dict, add_employee):
        t = add_employee(arg_dict)
        t.execute()
        employee = DB.get_employee(DB, arg_dict['emp_id'])
        for attr_name, attr_value in arg_dict.items():
            self.assertTrue(getattr(employee, attr_name) == attr_value)
        return employee

    def setUp(self) -> None:
        self.arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
            'commission_rate': 0.1
        }
        self.employee = self.new_employee(
            arg_dict=self.arg_dict,
            add_employee=AddCommissionedEmployee
        )

        self.arg_dict2 = {
            'emp_id': 2,
            'name': "김재희",
            'address': "파주",
            'hourly_rate': 1.0
        }
        self.employee2 = self.new_employee(
            arg_dict=self.arg_dict2,
            add_employee=AddHourlyEmployee
        )

        self.cc = self.employee.classification
        self.assertIsInstance(self.cc, CommissionedClassification)

    def tearDown(self) -> None:
        DB.clear(DB)

    def test_transaction(self):
        t = SalesReceiptTransaction(
            emp_id=self.arg_dict['emp_id'],
            date=20011031,
            amount=8.0
        )
        t.execute()

        sr = self.cc.get_sales(20011031)
        self.assertIsInstance(sr, SalesReceipt)
        self.assertEqual(sr.amount, 8.0)

    def test_wrong_id(self):
        with self.assertRaises(NoEmployeeError):
            t = SalesReceiptTransaction(
                emp_id=987,
                date=20011031,
                amount=8.0
            )
            t.execute()

    def test_wrong_employee(self):
        with self.assertRaises(NotCommissionedError):
            t = SalesReceiptTransaction(
                emp_id=2,
                date=20011031,
                amount=8.0
            )
            t.execute()

    def test_get_wrong_date(self):
        with self.assertRaises(NoSalesError):
            tc = self.cc.get_sales(99990909)
