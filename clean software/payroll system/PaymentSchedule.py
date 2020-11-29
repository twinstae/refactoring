from abc import *
import calendar
from datetime import date


class PaymentSchedule(metaclass=ABCMeta):
    pass


class MonthlySchedule(PaymentSchedule):
    @staticmethod
    def is_pay_day(pay_date: date):
        return pay_date.day == calendar.monthrange(pay_date.year, pay_date.month)[1]


class WeeklySchedule(PaymentSchedule):
    pass


class BiweeklySchedule(PaymentSchedule):
    pass
