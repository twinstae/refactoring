class PrimeCalculator:
    is_crossed = []

    def generate_primes(self, max_value):
        if max_value + 1 > 2:
            self.is_crossed = [False] * (max_value + 1)

            for i in range(2, int(len(self.is_crossed) ** 0.5 + 1)):
                if not self.is_crossed[i]:
                    self.crossed_multiples(i)

            return self.uncross_int_to_result()
        return []

    def crossed_multiples(self, i):
        for j in range(2 * i, len(self.is_crossed), i):
            self.is_crossed[j] = True

    def uncross_int_to_result(self):
        return [i for i, is_prime in enumerate(self.is_crossed[2:], start=2) if not is_prime]


if __name__ == '__main__':
    calc = PrimeCalculator()
    if not calc.generate_primes(0):
        print("테스트 통과, 0이하의 소수는 없다")

    if [2] == calc.generate_primes(2):
        print("테스트 통과. 2 이하의 소수는 [2] 뿐이다.")
    else:
        print("테스트 실패", calc.generate_primes(2))

    prime_list = [2, 3, 5, 7, 11, 13, 17, 19]
    passed = True
    for a, b in zip(prime_list, calc.generate_primes(20)):
        if a != b:
            print("test 실패", a, "=/=", b)
            passed = False
    if passed:
        print("테스트 통과. 20이하의 소수")
