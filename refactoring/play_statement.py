from jinja2 import Environment, PackageLoader, select_autoescape, Template, FileSystemLoader

from create_data import Data

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


def statement(invoices):
    return render_plain_text(
        data=Data(invoices).result
    )


def statement_html(invoices):
    template = env.get_template('statement.html')
    return template.render(
        data=Data(invoices).result
    )


def render_plain_text(data):
    result = '청구내역 (고객명 : %s)\n' % (data["customer"])
    for perf in data['performances']:
        result += '    %s: %s (%s석)\n' % (perf['play']['name'], perf['amount'] / 100, perf['audience'])
    result += "총액: %s\n" % (data['total_amount'] / 100)
    result += "적립 포인트: %s 점" % data['total_volume_credits']
    return result
