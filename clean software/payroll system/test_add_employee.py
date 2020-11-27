import unittest

from Employee import SalariedClassification, HourlyClassification
from PaymentMethod import HoldMethod
from PaymentSchedule import MonthlySchedule, WeeklySchedule
from PayrollDB import PayrollDB as DB
from main import AddSalariedEmployee, AddHourlyEmployee


class TestAddEmployee(unittest.TestCase):

    def test_add_salaried_employee(self):
        emp_id = 1
        t = AddSalariedEmployee(emp_id, "김태희", "파주", 1000.0)
        t.execute()

        employee = DB.get_employee(DB, emp_id)
        self.assertEqual(employee.name, "김태희")
        self.assertEqual(employee.salary, 1000.0)

        self.classification_schedule_method(
            employee,
            classification=SalariedClassification,
            schedule=MonthlySchedule,
            method=HoldMethod
        )

    def test_add_hourly_employee(self):
        emp_id = 1
        t = AddHourlyEmployee(emp_id, "김태희", "파주", 1.0)
        t.execute()

        employee = DB.get_employee(DB, emp_id)
        self.assertEqual(employee.name, "김태희")
        self.assertEqual(employee.hourly_rate, 1.0)

        self.classification_schedule_method(
            employee,
            classification=HourlyClassification,
            schedule=WeeklySchedule,
            method=HoldMethod
        )

    def classification_schedule_method(self, employee, classification, schedule, method):
        pc = employee.classification
        self.assertIsInstance(pc, classification)

        ps = employee.schedule
        self.assertIsInstance(ps, schedule)

        pm = employee.method
        self.assertIsInstance(pm, method)


if __name__ == '__main__':
    unittest.main()
