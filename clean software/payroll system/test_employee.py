import unittest

from Employee import SalariedClassification, HourlyClassification, CommissionedClassification, NoNameError, \
    NoAddressError
from PaymentMethod import pay_hold
from PaymentSchedule import is_weekly_friday, is_monthly_friday, is_biweekly_pay_day
from PayrollDB import PayrollDB as DB, NoEmployeeError
from Tranaction import DeleteEmployee, NoHourlyError, NoEmpIdError, add_hourly_employee_transaction, \
    add_salaried_employee_transaction, add_commissioned_employee_transaction


class TestEmployee(unittest.TestCase):

    def test_add_hourly_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'hourly_rate': 1.0
        }
        transaction = add_hourly_employee_transaction(arg_dict)
        transaction()
        employee = self.validate_get_employee(arg_dict)

        self.classification_schedule_method(
            employee,
            classification=HourlyClassification,
            schedule=is_weekly_friday,
            pay_method=pay_hold
        )

    def raise_assert(self, e):
        with self.assertRaises(e):
            transaction = add_hourly_employee_transaction(self.arg_dict)
            transaction()

    def test_add_wrong_hourly_employee(self):
        self.arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'rate_hour': 1.0
        }
        self.raise_assert(NoHourlyError)

    def test_add_wrong_name_employee(self):
        self.arg_dict = {
            'emp_id': 1,
            'title': "김태희",
            'address': "파주",
            'hourly_rate': 1.0
        }
        self.raise_assert(NoNameError)

    def test_add_wrong_address_employee(self):
        self.arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'addres': "파주",
            'hourly_rate': 1.0
        }
        self.raise_assert(NoAddressError)

    def test_add_wrong_id_employee(self):
        self.arg_dict = {
            'id': 1,
            'title': "김태희",
            'address': "파주",
            'hourly_rate': 1.0
        }
        self.raise_assert(NoEmpIdError)

    def test_add_salaried_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
        }
        transaction = add_salaried_employee_transaction(arg_dict)
        transaction()
        employee = self.validate_get_employee(arg_dict)

        self.classification_schedule_method(
            employee,
            classification=SalariedClassification,
            schedule=is_monthly_friday,
            pay_method=pay_hold
        )

    def test_commissioned_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
            'commission_rate': 0.1
        }
        transaction = add_commissioned_employee_transaction(arg_dict)
        transaction()
        employee = self.validate_get_employee(arg_dict)

        self.classification_schedule_method(
            employee,
            classification=CommissionedClassification,
            schedule=is_biweekly_pay_day,
            pay_method=pay_hold
        )

    def test_delete_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
            'commission_rate': 0.1
        }
        transaction = add_commissioned_employee_transaction(arg_dict)
        transaction()
        employee = self.validate_get_employee(arg_dict)

        self.assertEqual(
            DB.get_employee(arg_dict['emp_id']), employee
        )

        t = DeleteEmployee(arg_dict['emp_id'])
        t.execute()

        with self.assertRaises(NoEmployeeError):
            DB.get_employee(arg_dict['emp_id'])

    def validate_get_employee(self, arg_dict):
        employee = DB.get_employee(arg_dict['emp_id'])
        for attr_name, attr_value in arg_dict.items():
            self.assertTrue(getattr(employee, attr_name) == attr_value)
        return employee

    def classification_schedule_method(self, employee, classification, schedule, pay_method):
        pc = employee.classification
        self.assertIsInstance(pc, classification)

        ps = employee.schedule
        self.assertEqual(ps, schedule)

        pm = employee.pay_method
        self.assertEqual(pm, pay_method)


if __name__ == '__main__':
    unittest.main()
