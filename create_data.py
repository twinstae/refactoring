play_data = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}

def create_data(invoice):
    def amount_for(perf):
        play = perf['play']
        result = 0
        if play['type'] == "tragedy":
            result = 40000
            if perf["audience"] > 30:
                result += 1000 * (perf["audience"] - 30)
        elif play['type'] == "comedy":
            result = 30000
            if perf["audience"] > 20:
                result += 10000 + 500 * (perf["audience"] - 20)
        return result

    def volume_credit_for(perf):
        result = max(perf["audience"] - 30, 0)
        if "comedy" == perf['play']['type']:
            result += perf['audience'] // 5
        return result

    def total_amount():
        return sum([p['amount'] for p in data['performances']])

    def total_volume_credits():
        return sum([p['credit'] for p in data['performances']])

    data = {
        "customer": invoice["customer"],
        "performances": invoice["performances"].copy()
    }

    for perf in data['performances']:
        perf['play'] = play_data[perf["playID"]]
        perf['amount'] = amount_for(perf)
        perf['credit'] = volume_credit_for(perf)

    data["total_amount"] = total_amount()
    data["total_volume_credits"] = total_volume_credits()
    return data
