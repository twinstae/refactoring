class Employee:
    def __init__(self, arg_dict, classification, schedule, method):
        for attr_name, value in arg_dict.items():
            setattr(self, attr_name, value)
        self.classification = classification
        self.schedule = schedule
        self.method = method
        self.affiliation = None

    def set_affiliation(self, affiliation):
        self.affiliation = affiliation


class PaymentClassification:
    pass


class HourlyClassification(PaymentClassification):
    def __init__(self, hourly_rate):
        self.hourly_rate = hourly_rate
        self._time_card_dict = {}

    def get_time_card(self, date):
        if date not in self._time_card_dict:
            raise NoTimeCardError
        return self._time_card_dict[date]

    def add_time_card(self, time_card):
        self._time_card_dict[time_card.date] = time_card


class NoTimeCardError(Exception):
    def __str__(self):
        return "date에 time_card가 없습니다"


class CommissionedClassification(PaymentClassification):
    def __init__(self, salary, commission_rate):
        self.salary = salary
        self.commission_rate = commission_rate
        self._sales_dict = {}

    def get_sales(self, date):
        if date not in self._sales_dict:
            raise NoSalesError
        return self._sales_dict[date]

    def add_sales(self, sales):
        self._sales_dict[sales.date] = sales


class SalariedClassification(PaymentClassification):
    def __init__(self, salary):
        self.salary = salary


class NoSalesError(Exception):
    def __str__(self):
        return "date에 sales가 없습니다"

