import unittest
from play_statement import statement, statement_html
from create_data import Data, PLAY_DATA, play_for, create_calc, TragedyCalculator, ComedyCalculator

HAMLET = {
            "playID": "hamlet",
            "audience": 55
        }
AS_LIKE = {
            "playID": "as-like",
            "audience": 35
        }

OTHELLO = {
            "playID": "othello",
            "audience": 40
        }

INVOICES = {
    "customer": "BigCo",
    "performances": [
        HAMLET,
        AS_LIKE,
        OTHELLO
    ]
}

ANSWER = """청구내역 (고객명 : BigCo)
    Hamlet: 650.0 (55석)
    As You Like It: 475.0 (35석)
    Othello: 500.0 (40석)
총액: 1625.0
적립 포인트: 47 점"""

ANSWER_HTML = """<h1>청구내역 (고객명 : BigCo)</h1>
<table>
<tr><th>연국</th><th>좌석</th><th>금액</th></tr>
    <tr><th>Hamlet</th><th>55</th><th>65000</th></tr>
    <tr><th>As You Like It</th><th>35</th><th>47500</th></tr>
    <tr><th>Othello</th><th>40</th><th>50000</th></tr>
</table>
<p>총액: 162500</p>
<p>적립 포인트: 47 점</p>"""


class TestPay(unittest.TestCase):

    def test_statement(self):
        for expected, actual in zip(ANSWER.split("\n"), statement(INVOICES).split("\n")):
            self.assertEqual(expected, actual)

    def test_statement_html(self):
        for expected, actual in zip(
                ANSWER_HTML.split("\n"),
                statement_html(INVOICES).replace("\n\n", "\n").split("\n")
        ):
            self.assertEqual(expected, actual)

    def setUp(self) -> None:
        self.data = Data(INVOICES)
        self.result = self.data.result

    def test_play_for_tragedy(self):
        self.assertEqual(PLAY_DATA['hamlet'], play_for(HAMLET))

    def test_play_for_comedy(self):
        self.assertEqual(PLAY_DATA['as-like'], play_for(AS_LIKE))

    def test_calc_tragedy(self):
        self.assertIsInstance(create_calc(HAMLET), TragedyCalculator)

    def test_calc_comedy(self):
        self.assertIsInstance(create_calc(AS_LIKE), ComedyCalculator)

    def test_calc_amount_tragedy(self):
        hamlet_calc = create_calc(HAMLET)
        self.assertEqual(65000, hamlet_calc.amount())

    def test_calc_credit_tragedy(self):
        hamlet_calc = create_calc(HAMLET)
        self.assertEqual(25, hamlet_calc.volume_credit())

    def test_calc_amount_comedy(self):
        as_like_calc = create_calc(AS_LIKE)
        self.assertEqual(47500, as_like_calc.amount())

    def test_calc_credit_comedy(self):
        as_like_calc = create_calc(AS_LIKE)
        self.assertEqual(12, as_like_calc.volume_credit())

    def test_values_total(self):
        self.assertEqual(self.data.values('amount'), [65000, 47500, 50000])
        self.assertEqual(self.result['total_amount'], 162500)

    def test_credit_total(self):
        self.assertEqual(self.data.values('credit'), [25, 12, 10])
        self.assertEqual(self.result['total_volume_credits'], 47)
