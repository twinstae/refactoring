class Employee:
    def __init__(self,emp_id, name, address):
        self.emp_id = emp_id
        self.name = name
        self.address = address


class PaymentClassification:
    pass

class HourlyClassification(PaymentClassification):
    pass

class CommissionedClassification(PaymentClassification):
    pass

class SalariedClassification(PaymentClassification):
    pass