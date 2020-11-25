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

    result = '청구내역 (고객명 : %s)\n' % (invoice["customer"])

    for perf in invoice["performances"]:
        play = play_for(perf)
        result += '    %s: %s (%s석)\n' % (play['name'], amount_for(perf) / 100, perf['audience'])

    result += "총액: %s\n" % (total_amount(invoice) / 100)
    result += "적립 포인트: %s 점" % total_volume_credits(invoice)

    return result


def total_amount(invoice):
    result = 0
    for perf in invoice["performances"]:
        result += amount_for(perf)
    return result


def total_volume_credits(invoice):
    volume_credits = 0
    for perf in invoice["performances"]:
        volume_credits += volume_credit_for(perf)
    return volume_credits


def volume_credit_for(perf):
    result = max(perf["audience"] - 30, 0)
    if "comedy" == play_for(perf)['type']:
        result += perf['audience'] // 5
    return result


def play_for(perf):
    return play_data[perf["playID"]]


def amount_for(perf):
    play = play_for(perf)
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
