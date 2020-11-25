from create_data import create_data

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
    data = create_data(invoice)
    return render_plain_text(data)


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
