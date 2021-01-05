import unittest
from play_statement import statement
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


class TestPay(unittest.TestCase):

    def test_result(self):
        count = 0
        for a, r in zip(ANSWER.split("\n"), statement(INVOICES).split("\n")):
            count += 1
            self.assertEqual(a, r)
            print("테스트", count, "PASS")
        print("!!!초록 막대!!!")

    def setUp(self) -> None:
        self.data = Data(INVOICES)
        self.result = self.data.result

    def test_play_for(self):
        self.assertEqual(PLAY_DATA['hamlet'], play_for(HAMLET))
        self.assertEqual(PLAY_DATA['as-like'], play_for(AS_LIKE))

    def test_calc(self):
        self.assertIsInstance(create_calc(HAMLET), TragedyCalculator)
        self.assertIsInstance(create_calc(AS_LIKE), ComedyCalculator)

    def test_calc_amount(self):
        hamlet = HAMLET.copy()
        hamlet_calc = create_calc(hamlet)
        self.assertEqual(65000, hamlet_calc.amount())

        as_like = AS_LIKE.copy()
        as_like_calc = create_calc(as_like)
        self.assertEqual(47500, as_like_calc.amount())

    def test_values_total(self):
        self.assertEqual(self.data.values('amount'), [65000, 47500, 50000])
        self.assertEqual(self.data.values('credit'), [25, 12, 10])

        self.assertEqual(self.result['total_amount'], 162500)
        self.assertEqual(self.result['total_volume_credits'], 47)
