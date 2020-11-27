class Employee:
    def __init__(self, emp_id, name, address, classification, schedule, method):
        self.emp_id = emp_id
        self.name = name
        self.address = address
        self.classification = classification
        self.schedule = schedule
        self.method = method


class PaymentClassification:
    pass


class HourlyClassification(PaymentClassification):
    def __init__(self, hourly_rate):
        self.hourly_rate = hourly_rate
        self._time_card_dict = {}

    def get_time_card(self, date):
        return self._time_card_dict.get(date, None)

    def add_time_card(self, time_card):
        self._time_card_dict[time_card.date] = time_card


class CommissionedClassification(PaymentClassification):
    def __init__(self, salary, commission_rate):
        self.salary = salary
        self.commission_rate = commission_rate
        self._sales_dict = {}

    def get_sales(self, date):
        return self._sales_dict.get(date, None)

    def add_sales(self, sales):
        self._sales_dict[sales.date] = sales


class SalariedClassification(PaymentClassification):
    def __init__(self, salary):
        self.salary = salary

