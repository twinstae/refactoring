from abc import *


class PaymentMethod(metaclass=ABCMeta):
    @staticmethod
    def pay(pc):
        pass


class HoldMethod(PaymentMethod):
    @staticmethod
    def pay(pc):
        pc.disposition = "Hold"


class DirectMethod(PaymentMethod):
    @staticmethod
    def pay(pc):
        pass


class MailMethod(PaymentMethod):
    @staticmethod
    def pay(pc):
        pass
