class PrimeCalculator:
    f = []

    def init_f(self, max_value):
        self.f = [True] * (max_value + 1)

    def generate_primes(self, max_value):
        if max_value + 1 > 2:
            self.init_f(max_value)
            self.find_prime()
            return self.extract_prime()
        return []

    def find_prime(self):
        self.f[0] = False
        self.f[1] = False
        for i in range(2, int(len(self.f) ** 0.5)):
            if self.f[i]:
                for j in range(2 * i, len(self.f), i):
                    self.f[j] = False

    def extract_prime(self):
        return [i for i, is_prime in enumerate(self.f) if is_prime]


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
