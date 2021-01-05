import unittest
from play_statement import statement
from create_data import Data, PLAY_DATA, play_for

HAMLET = {
            "playID": "hamlet",
            "audience": 55
        }

INVOICES = {
    "customer": "BigCo",
    "performances": [
        HAMLET,
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
        self.data = Data(INVOICES).result()

    def test_play_for(self):
        self.assertEqual(PLAY_DATA['hamlet'], play_for(hamlet))

    def test_calc(self):

    def test_data(self):
        self.assertEqual(self.data['total_amount'], 162500)
        self.assertEqual(self.data['total_volume_credits'], 47)
