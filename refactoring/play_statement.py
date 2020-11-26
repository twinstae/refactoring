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


def statement(invoices):
    return render_plain_text(create_data(invoices))


def render_html(data):
    result = '<h1>청구내역 (고객명 : %s)</h1>\n' % (data["customer"])
    result += '<table>\n'
    result += '<tr><th>연국</th><th>좌석</th><th>금액</th></tr>'
    for perf in data['performances']:
        result += '<tr><th>%s</th><th>%s</th><th>%s석</th></tr>\n'\
                  % (perf['play']['name'], perf['audience'], perf['amount'] / 100)
    result += '</table>\n'
    result += "<p>총액: %s</p>" % (data['total_amount'] / 100)
    result += "<p>적립 포인트: %s 점</p>" % data['total_volume_credits']
    return result


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

count = 0
for a, r in zip(answer.split("\n"), statement(invoices).split("\n")):
    count += 1
    if a != r:
        print("test 실패...")
        print(a)
        print(r)
        passed = False
    else:
        print("테스트", count, "PASS")
if passed:
    print("!!!초록 막대!!!")
