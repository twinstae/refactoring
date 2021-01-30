import unittest

from ChangeEmployeeTransaction import ChangeNameTransaction, ChangeAddressTransaction, ChangeSalariedTransaction, \
    ChangeHourlyTransaction, ChangeCommissionedTransaction
from Employee import HourlyClassification, SalariedClassification, CommissionedClassification
from PayrollDB import PayrollDB as DB, NoEmployeeError
from PaymentSchedule import is_weekly_friday, is_biweekly_pay_day, is_monthly_friday
from Tranaction import add_hourly_employee_transaction, add_commissioned_employee_transaction


class TestChangeEmployee(unittest.TestCase):

    def setUp(self) -> None:
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'hourly_rate': 1.0
        }
        transaction = add_hourly_employee_transaction(arg_dict)
        transaction()
        self.hourly_id = arg_dict['emp_id']

        arg_dict2 = {
            'emp_id': 2,
            'name': "김재희",
            'address': "파주",
            'salary': 1000.0,
            'commission_rate': 0.1
        }
        transaction_2 = add_commissioned_employee_transaction(arg_dict2)
        transaction_2()
        self.commission_id = arg_dict2['emp_id']

    def tearDown(self) -> None:
        DB.clear()

    def validate_get_employee(self, arg_dict):
        employee = DB.get_employee(arg_dict['emp_id'])
        for attr_name, attr_value in arg_dict.items():
            self.assertTrue(getattr(employee, attr_name) == attr_value)
        return employee

    def test_change_name(self):
        new_name = "Bob"
        t = ChangeNameTransaction(
            emp_id=self.hourly_id,
            new_name=new_name
        )
        t.execute()
        new_employee = DB.get_employee(emp_id=self.hourly_id)
        self.assertEqual(new_employee.name, new_name)

    def test_change_address(self):
        new_address = "서울"
        t = ChangeAddressTransaction(
            emp_id=self.hourly_id,
            new_address=new_address
        )
        t.execute()
        new_employee = DB.get_employee(emp_id=self.hourly_id)
        self.assertEqual(new_employee.address, new_address)

    def test_change_wrong_employee(self):
        new_value = "의미 없는 값"
        transaction_list = [
            ChangeAddressTransaction,
            ChangeNameTransaction,
            ChangeSalariedTransaction,
            ChangeHourlyTransaction
        ]
        for transaction in transaction_list:
            with self.assertRaises(NoEmployeeError):
                t = transaction(987, new_value)
                t.execute()

    def test_change_hourly(self):
        t = ChangeHourlyTransaction(self.commission_id, 10)
        self.change_cls(
            t,
            HourlyClassification,
            is_weekly_friday
        )

    def test_change_salaried(self):
        t = ChangeSalariedTransaction(self.hourly_id, 1000)
        self.change_cls(
            t,
            SalariedClassification,
            is_monthly_friday
        )

    def test_change_commissioned(self):
        t = ChangeCommissionedTransaction(self.hourly_id, 1000, 0.1)
        self.change_cls(
            t,
            CommissionedClassification,
            is_biweekly_pay_day
        )

    def change_cls(self, t, cls, schedule_cls):
        t.execute()
        new_employee = DB.get_employee(emp_id=t.emp_id)
        self.assertIsInstance(new_employee.classification, cls)
        self.assertEqual(new_employee.schedule, schedule_cls)


if __name__ == '__main__':
    unittest.main()
