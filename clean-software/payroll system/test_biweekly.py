import unittest
from datetime import date, timedelta

from PaymentSchedule import is_weekly_friday, is_biweekly_pay_day


class TestPay(unittest.TestCase):
    def test_weekly(self):
        start_date = date(2000, 1, 7)
        self.assertEqual(start_date.weekday(), 4)
        self.assertTrue(is_weekly_friday(start_date))

    def test_biweekly(self):
        start_date = date(2000, 1, 14)
        for i in range(2000):  # 40년 동안 문제 없는지?
            new_date = start_date + timedelta(days=7*i)
            self.assertTrue(is_biweekly_pay_day(new_date) == bool(i % 2), msg=f"{i} {new_date}")
