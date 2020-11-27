import unittest
from main import PayrollSystem

sample_transaction = [
    # 직원 추가
    # 명령    번호 이름  주소 코드   수수료율
    'AddEmp 001 김태희 파주 H 시급',
    'AddEmp 002 김재희 파주 S 월급',
    'AddEmp 003 김희선 파주 C 월급 0.2',
    'AddEmp 123 홍길동 파주 J 월급 0.2',  # 양식에 맞지 않으면 에러
    # 직원 삭제
    'DelEmp 003',
    'DelEmp 465798',  # 없는 직원은 에러 메세지 출력
    'DeleteEmp 465798',  # 양식에 맞지 않으면 에러
    # 타임 카드 추가
    'TimeCard 001 11/27 8.5',
    'TimeCard 002 11/27 8.5',  # 월급쟁이는 에러 출력
    'TimeCard 321 11/27 8.5',  # 없는 직원은 에러 출력
    # 판매 영수증 기록
    'SaleReceipt 003 11/27 100000',
    'SaleReceipt 002 11/27 100000',  # 수수료 안 받는 직원은 에러
    'SaleReceipt 321 11/27 100000',  # 없는 직원은 에러
    # 조합 공제액 기록
    'ServiceCharge 001 100000',
    'ServiceCharge 321 100000',  # 없는 직원은 에러
    # 직원 정보 변경
    'ChgEmp 001 Name 정호영',
    'ChgEmp 001 Member 1 Dues 0.01',
    'ChgEmp 001 Member 1 Dues 0.01',  # 이미 조합원인데 또 넣으려 하면 에러
    'ChgEmp 321 Member 1 Dues 0.01',  # 없는 직원은 에러
    'ChgEmp 001 NoMember',
    'ChgEmp 321 NoMember',  # 없는 직원은 에러
    'Payday 12/20', # 임금을 받는 직원 목록
]


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


if __name__ == '__main__':
    unittest.main()