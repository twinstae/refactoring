import unittest

from Employee import HourlyClassification
from PayrollDB import PayrollDB as DB
from TimeCard import TimeCard
from Tranaction import AddHourlyEmployee, TimeCardTransaction


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
            'hourly_rate': 1.0
        }
        self.employee = self.new_employee(
            arg_dict=self.arg_dict,
            add_employee=AddHourlyEmployee
        )

    def tearDown(self) -> None:
        DB.clear(DB)

    def test_add_and_get_time_card(self):
        t = TimeCardTransaction(
            emp_id=self.arg_dict['emp_id'],
            date=20011031,
            hours=8.0
        )
        t.execute()
        hc = self.employee.classification
        self.assertIsInstance(hc, HourlyClassification)

        tc = hc.get_time_card(20011031)
        self.assertIsInstance(tc, TimeCard)
        self.assertEqual(tc.hours, 8.0)

    def test_add_and_get_wrong_time_card(self):
        t = TimeCardTransaction(
            emp_id=987,
            date=20011031,
            hours=8.0
        )
        msg = t.execute()
        self.assertEqual(msg, "id 없음 : 해당하는 employee가 DB에 없습니다.")

        hc = self.employee.classification
        self.assertIsInstance(hc, HourlyClassification)

        tc = hc.get_time_card(99990909)
        self.assertEqual(tc, None)


if __name__ == '__main__':
    unittest.main()
