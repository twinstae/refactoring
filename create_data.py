play_data = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}


class PerfCalculator:
    def __init__(self, a_perf, a_play):
        self.perf = a_perf
        self.play = a_play

    def amount(self):
        result = 0
        if self.play['type'] == "tragedy":
            print("error!!!!")
            raise Exception
        elif self.play['type'] == "comedy":
            result = 30000
            if self.perf["audience"] > 20:
                result += 10000 + 500 * (self.perf["audience"] - 20)
        return result

    def volume_credit(self):
        result = max(self.perf["audience"] - 30, 0)
        if "comedy" == self.perf['play']['type']:
            result += self.perf['audience'] // 5
        return result


class TragedyCalculator(PerfCalculator):
    def amount(self):
        result = 40000
        if self.perf["audience"] > 30:
            result += 1000 * (self.perf["audience"] - 30)
        return result


def play_for(perf):
    return play_data[perf["playID"]]


def create_calc(perf):
    if play_for(perf)['type'] == 'tragedy':
        return TragedyCalculator(perf, play_for(perf))
    return PerfCalculator(perf, play_for(perf))


def create_data(invoice):
    def total_amount():
        return sum([p['amount'] for p in data['performances']])

    def total_volume_credits():
        return sum([p['credit'] for p in data['performances']])

    data = {
        "customer": invoice["customer"],
        "performances": invoice["performances"].copy()
    }

    for perf in data['performances']:  # enrich perf
        calc = create_calc(perf)
        perf['play'] = play_for(perf)
        perf['amount'] = calc.amount()
        perf['credit'] = calc.volume_credit()

    data["total_amount"] = total_amount()
    data["total_volume_credits"] = total_volume_credits()
    return data
