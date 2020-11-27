from abc import *


class PaymentMethod(metaclass=ABCMeta):
    pass

class HoldMethod(PaymentMethod):
    pass

class DirectMethod(PaymentMethod):
    pass

class MailMethod(PaymentMethod):
    pass