def generate_primes(max_value):
    if max_value >= 2:
        s = max_value + 1
        f = [True] * s  # 파이써닉한 꼼수
        f[0] = False
        f[1] = False

        for i in range(2, int(s**0.5)):
            if f[i]:
                for j in range(2*i, s, i):
                    f[j] = False

        count = sum(f)  # 파이써닉한 꼼수2. 사실 리스트는 동적 배열이라 필요도 없다.

        primes = [i for i in range(s) if f[i]]
        return primes
    return []


if __name__ == '__main__':
    if not generate_primes(0):
        print("테스트 통과, 0이하의 소수는 없다")

    if [2] == generate_primes(2):
        print("테스트 통과. 2 이하의 소수는 [2] 뿐이다.")
    else:
        print("테스트 실패")

    prime_list = [2, 3, 5, 7, 11, 13, 17, 19]
    for a, b in zip(prime_list, generate_primes(20)):
        if a == b:
            print("test", a, "통과")
        else:
            print("test 실패", a, "=/=", b)
