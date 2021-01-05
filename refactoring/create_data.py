PLAY_DATA = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}


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


def play_for(perf):
    return PLAY_DATA[perf["playID"]]


def create_calc(perf):
    perf_type = play_for(perf)['type']
    if perf_type == 'tragedy':
        return TragedyCalculator(perf)
    if perf_type == 'comedy':
        return ComedyCalculator(perf)
    raise Exception


class Data:
    def __init__(self, invoice):
        self.result = invoice.copy()
        for perf in self.result['performances']:  # enrich perf
            perf['play'] = play_for(perf)

            calc = create_calc(perf)
            perf['amount'] = calc.amount()
            perf['credit'] = calc.volume_credit()

        self.result["total_amount"] = sum(self.values('amount'))
        self.result["total_volume_credits"] = sum(self.values('credit'))

    def result(self):
        return self.result

    def values(self, key):
        return [p[key] for p in self.result['performances']]
