import calendar
from datetime import date


def is_monthly_friday(target_date: date):
    return target_date.day == calendar.monthrange(target_date.year, target_date.month)[1]


def is_weekly_friday(target_date: date):
    return target_date.weekday() == 4


def is_biweekly_pay_day(target_date: date):
    first_day = date(2000, 1, 1)
    return (target_date - first_day).days % 14 == 6
