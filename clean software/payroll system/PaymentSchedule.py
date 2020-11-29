from abc import *
import calendar
from datetime import date, timedelta


class PaymentSchedule(metaclass=ABCMeta):
    pass


class MonthlySchedule(PaymentSchedule):
    @staticmethod
    def is_pay_day(pay_date: date):
        return pay_date.day == calendar.monthrange(pay_date.year, pay_date.month)[1]


def is_friday(pay_date):
    return pay_date.weekday() == 4


class WeeklySchedule(PaymentSchedule):
    @staticmethod
    def is_pay_day(pay_date: date):
        return is_friday(pay_date)


def is_biweek(target):
    first_day = date(2000, 1, 1)
    return (target - first_day).days % 14 == 6


class BiweeklySchedule(PaymentSchedule):
    @staticmethod
    def is_pay_day(pay_date: date):
        return is_biweek(pay_date)
