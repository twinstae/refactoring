import unittest

from Employee import CommissionedClassification
from PayrollDB import PayrollDB as DB
from SalesReceipt import SalesReceipt
from Tranaction import SalesReceiptTransaction, AddCommissionedEmployee, AddHourlyEmployee


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

    def tearDown(self) -> None:
        DB.clear(DB)

    def test_transaction(self):
        t = SalesReceiptTransaction(
            emp_id=self.arg_dict['emp_id'],
            date=20011031,
            amount=8.0
        )
        t.execute()
        cc = self.employee.classification
        self.assertIsInstance(cc, CommissionedClassification)

        sr = cc.get_sales(20011031)
        self.assertIsInstance(sr, SalesReceipt)
        self.assertEqual(sr.amount, 8.0)

    def test_wrong_id(self):
        t = SalesReceiptTransaction(
            emp_id=987,
            date=20011031,
            amount=8.0
        )
        msg = t.execute()
        self.assertEqual(msg, "id 없음 : 해당하는 employee가 DB에 없습니다.")

    def test_wrong_employee(self):
        t = SalesReceiptTransaction(
            emp_id=2,
            date=20011031,
            amount=8.0
        )
        msg = t.execute()
        self.assertEqual(msg, "she/he is not a commissioned employee")

    def test_get_wrong_date(self):
        cc = self.employee.classification
        self.assertIsInstance(cc, CommissionedClassification)

        tc = cc.get_sales(99990909)
        self.assertEqual(tc, None)
