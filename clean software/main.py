def generate_primes(max_value):
    if max_value >= 2:
        f = init(max_value)  # 파이써닉한 꼼수

        for i in range(2, int(len(f) ** 0.5)):
            if f[i]:
                for j in range(2 * i, len(f), i):
                    f[j] = False

        primes = extract_prime(f)
        return primes
    return []


def init(max_value):
    f = [True] * (max_value + 1)
    f[0] = False
    f[1] = False
    return f


def extract_prime(f):
    return [i for i in range(len(f)) if f[i]]


if __name__ == '__main__':
    if not generate_primes(0):
        print("테스트 통과, 0이하의 소수는 없다")

    if [2] == generate_primes(2):
        print("테스트 통과. 2 이하의 소수는 [2] 뿐이다.")
    else:
        print("테스트 실패")

    prime_list = [2, 3, 5, 7, 11, 13, 17, 19]
    passed = True
    for a, b in zip(prime_list, generate_primes(20)):
        if a != b:
            print("test 실패", a, "=/=", b)
            passed = False
    if passed:
        print("테스트 통과. 20이하의 소수")
