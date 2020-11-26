def generate_primes(max_value):
    return [2, 3, 5, 7, 11, 13, 17, 19]


if __name__ == '__main__':
    prime_list = [2, 3, 5, 7, 11, 13, 17, 19]
    for a, b in zip(prime_list, generate_primes(20)):
        if a == b:
            print("test", a, "통과")
        else:
            print("test 실패", a, "=/=", b)
