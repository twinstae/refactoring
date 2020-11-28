import unittest

from Employee import SalariedClassification, HourlyClassification, CommissionedClassification
from PaymentMethod import HoldMethod
from PaymentSchedule import MonthlySchedule, WeeklySchedule, BiweeklySchedule
from PayrollDB import PayrollDB as DB
from Tranaction import AddSalariedEmployee, AddHourlyEmployee, AddCommissionedEmployee, DeleteEmployee


class TestEmployee(unittest.TestCase):

    def test_add_hourly_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'hourly_rate': 1.0
        }
        t = AddHourlyEmployee(arg_dict)
        t.execute()
        employee = self.validate_get_employee(arg_dict)

        self.classification_schedule_method(
            employee,
            classification=HourlyClassification,
            schedule=WeeklySchedule,
            method=HoldMethod
        )

    def test_add_wrong_hourly_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'rate_hour': 1.0
        }
        t = AddHourlyEmployee(arg_dict)
        e = t.execute()

        self.assertEqual(e, 'there is no hourly_rate')

    def test_add_salaried_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
        }
        t = AddSalariedEmployee(arg_dict)
        t.execute()
        employee = self.validate_get_employee(arg_dict)

        self.classification_schedule_method(
            employee,
            classification=SalariedClassification,
            schedule=MonthlySchedule,
            method=HoldMethod
        )

    def test_commissioned_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
            'commission_rate': 0.1
        }
        t = AddCommissionedEmployee(arg_dict)
        t.execute()
        employee = self.validate_get_employee(arg_dict)

        self.classification_schedule_method(
            employee,
            classification=CommissionedClassification,
            schedule=BiweeklySchedule,
            method=HoldMethod
        )

    def test_delete_employee(self):
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'salary': 1000.0,
            'commission_rate': 0.1
        }
        t = AddCommissionedEmployee(arg_dict)
        t.execute()
        employee = self.validate_get_employee(arg_dict)

        self.assertEqual(
            DB.get_employee(DB, arg_dict['emp_id']), employee
        )

        t = DeleteEmployee(arg_dict['emp_id'])
        t.execute()

        self.assertIsNone(
            DB.get_employee(DB, arg_dict['emp_id'])
        )

    def validate_get_employee(self, arg_dict):
        employee = DB.get_employee(DB, arg_dict['emp_id'])
        for attr_name, attr_value in arg_dict.items():
            self.assertTrue(getattr(employee, attr_name) == attr_value)
        return employee

    def classification_schedule_method(self, employee, classification, schedule, method):
        pc = employee.classification
        self.assertIsInstance(pc, classification)

        ps = employee.schedule
        self.assertIsInstance(ps, schedule)

        pm = employee.method
        self.assertIsInstance(pm, method)


if __name__ == '__main__':
    unittest.main()
