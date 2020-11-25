play_data = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}


class PerfCalculator:
    def __init__(self, a_perf, a_play):
        self.perf = a_perf
        self.play = a_play

    def amount_for(self):
        play = self.perf['play']
        result = 0
        if play['type'] == "tragedy":
            result = 40000
            if self.perf["audience"] > 30:
                result += 1000 * (self.perf["audience"] - 30)
        elif play['type'] == "comedy":
            result = 30000
            if self.perf["audience"] > 20:
                result += 10000 + 500 * (self.perf["audience"] - 20)
        return result

    def volume_credit_for(self):
        result = max(self.perf["audience"] - 30, 0)
        if "comedy" == self.perf['play']['type']:
            result += self.perf['audience'] // 5
        return result


def play_for(perf):
    return play_data[perf["playID"]]


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
        calc = PerfCalculator(perf, play_for(perf))
        perf['play'] = play_for(perf)
        perf['amount'] = calc.amount_for()
        perf['credit'] = calc.volume_credit_for()

    data["total_amount"] = total_amount()
    data["total_volume_credits"] = total_volume_credits()
    return data
