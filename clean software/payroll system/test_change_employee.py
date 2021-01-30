import unittest

from ChangeEmployeeTransaction import change_address_transaction, change_commissioned_transaction, \
    change_hourly_transaction, change_name_transaction, change_salaried_transaction
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
        transaction = change_name_transaction(
            emp_id=self.hourly_id,
            new_name=new_name
        )
        transaction()
        new_employee = DB.get_employee(emp_id=self.hourly_id)
        self.assertEqual(new_employee.name, new_name)

    def test_change_address(self):
        new_address = "서울"
        transaction = change_address_transaction(
            emp_id=self.hourly_id,
            new_address=new_address
        )
        transaction()
        new_employee = DB.get_employee(emp_id=self.hourly_id)
        self.assertEqual(new_employee.address, new_address)

    def test_change_wrong_employee(self):
        new_value = "의미 없는 값"
        transaction_list = [
            change_address_transaction,
            change_name_transaction,
            change_salaried_transaction,
            change_hourly_transaction
        ]
        for transaction_func in transaction_list:
            with self.assertRaises(NoEmployeeError):
                transaction = transaction_func(987, new_value)
                transaction()

    def test_change_hourly(self):
        transaction = change_hourly_transaction(self.commission_id, 10)
        self.change_cls(
            self.hourly_id,
            transaction,
            HourlyClassification,
            is_weekly_friday
        )

    def test_change_salaried(self):
        transaction = change_salaried_transaction(self.hourly_id, 1000)
        self.change_cls(
            self.hourly_id,
            transaction,
            SalariedClassification,
            is_monthly_friday
        )

    def test_change_commissioned(self):
        transaction = change_commissioned_transaction(self.hourly_id, 1000, 0.1)
        self.change_cls(
            self.hourly_id,
            transaction,
            CommissionedClassification,
            is_biweekly_pay_day
        )

    def change_cls(self, emp_id, transaction, cls, schedule_cls):
        transaction()
        new_employee = DB.get_employee(emp_id=emp_id)
        self.assertIsInstance(new_employee.classification, cls)
        self.assertEqual(new_employee.schedule, schedule_cls)


if __name__ == '__main__':
    unittest.main()
