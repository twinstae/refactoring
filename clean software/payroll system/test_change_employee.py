import unittest

from ChangeEmployeeTransaction import ChangeNameTransaction
from Employee import SalariedClassification, HourlyClassification, CommissionedClassification
from PaymentMethod import HoldMethod
from PaymentSchedule import MonthlySchedule, WeeklySchedule, BiweeklySchedule
from PayrollDB import PayrollDB as DB
from Tranaction import AddSalariedEmployee, AddHourlyEmployee, AddCommissionedEmployee, DeleteEmployee


class TestChangeEmployee(unittest.TestCase):

    def setUp(self) -> None:
        arg_dict = {
            'emp_id': 1,
            'name': "김태희",
            'address': "파주",
            'hourly_rate': 1.0
        }
        t = AddHourlyEmployee(arg_dict)
        t.execute()
        self.hourly_id = arg_dict['emp_id']

        arg_dict2 = {
            'emp_id': 2,
            'name': "김재희",
            'address': "파주",
            'salary': 1000.0,
            'commission_rate': 0.1
        }
        t2 = AddCommissionedEmployee(arg_dict2)
        t2.execute()
        self.commission_id = arg_dict2['emp_id']

    def tearDown(self) -> None:
        DB.clear(DB)

    def validate_get_employee(self, arg_dict):
        employee = DB.get_employee(DB, arg_dict['emp_id'])
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

        the_employee = DB.get_employee(DB, emp_id=self.hourly_id)

        self.assertEqual(the_employee.name, new_name)



if __name__ == '__main__':
    unittest.main()
