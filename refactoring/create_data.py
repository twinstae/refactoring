from Calculator import TragedyCalculator, ComedyCalculator

PLAY_DATA = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}


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

        self.result["total_amount"] = self.get_total('amount')
        self.result["total_volume_credits"] = self.get_total('credit')

    def values(self, key):
        return [p[key] for p in self.result['performances']]

    def get_total(self, key):
        return sum(self.values(key))
