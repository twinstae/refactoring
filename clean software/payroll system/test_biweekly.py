import unittest
from datetime import date, timedelta

from PaymentSchedule import BiweeklySchedule, WeeklySchedule


class TestPay(unittest.TestCase):
    def test_weekly(self):
        start_date = date(2000, 1, 7)
        self.assertEqual(start_date.weekday(), 4)
        ws = WeeklySchedule()
        self.assertTrue(ws.is_pay_day(start_date))

    def test_biweekly(self):
        start_date = date(2000, 1, 14)
        bws = BiweeklySchedule()
        for i in range(2000):  # 40년 동안 문제 없는지?
            new_date = start_date + timedelta(days=7*i)
            self.assertTrue(bws.is_pay_day(new_date) == bool(i % 2), msg=f"{i} {new_date}")
