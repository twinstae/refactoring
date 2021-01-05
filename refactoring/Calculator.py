class PerfCalculator:
    def __init__(self, a_perf):
        self.perf = a_perf

    def amount(self):
        raise Exception

    def volume_credit(self):
        return max(self.perf["audience"] - 30, 0)


class TragedyCalculator(PerfCalculator):
    def amount(self):
        return 40000 + self.surcharge()

    def surcharge(self):
        if self.perf["audience"] > 30:
            return 1000 * (self.perf["audience"] - 30)
        return 0


class ComedyCalculator(PerfCalculator):
    def amount(self):
        return 30000 + self.surcharge()

    def surcharge(self):
        if self.perf["audience"] > 20:
            return 10000 + 500 * (self.perf["audience"] - 20)
        return 0

    def volume_credit(self):
        return super().volume_credit() + self.perf['audience'] // 5
