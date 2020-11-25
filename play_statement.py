play_data = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}

invoices = {
    "customer": "BigCo",
    "performances": [
        {
            "playID": "hamlet",
            "audience": 55
        },
        {
            "playID": "as-like",
            "audience": 35
        },
        {
            "playID": "othello",
            "audience": 40
        }
    ]
}


def statement(invoice):
    data = make_data(invoice)
    return render_plain_text(data)

def make_data(invoice):
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

def render_plain_text(data):
    result = '청구내역 (고객명 : %s)\n' % (data["customer"])
    for perf in data['performances']:
        result += '    %s: %s (%s석)\n' % (perf['play']['name'], perf['amount'] / 100, perf['audience'])
    result += "총액: %s\n" % (data['total_amount'] / 100)
    result += "적립 포인트: %s 점" % data['total_volume_credits']
    return result


answer = """청구내역 (고객명 : BigCo)
    Hamlet: 650.0 (55석)
    As You Like It: 475.0 (35석)
    Othello: 500.0 (40석)
총액: 1625.0
적립 포인트: 47 점"""

passed = True

for a, r in zip(answer.split("\n"), statement(invoices).split("\n")):
    if a != r:
        print("test 실패...")
        print(a)
        print(r)
        passed = False
if passed:
    print("테스트 통과")
