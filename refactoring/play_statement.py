from create_data import Data


def statement(invoices):
    return render_plain_text(Data(invoices).result)


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
