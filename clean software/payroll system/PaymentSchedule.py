from abc import *


class PaymentSchedule(metaclass=ABCMeta):
    pass


class MonthlySchedule(PaymentSchedule):
    pass


class WeeklySchedule(PaymentSchedule):
    pass

class BiweeklySchedule(PaymentSchedule):
    pass
