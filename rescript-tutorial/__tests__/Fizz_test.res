open Jest
open TestUtil
open FizzBuzz

let expected_3_5_to_15 = `1
2
3 fizz
4
5 buzz
6 fizz
7
8
9 fizz
10 buzz
11
12 fizz
13
14
15 fizz buzz`

let expected_3_5_7_to_21 = `1
2
3 fizz
4
5 buzz
6 fizz
7 sezz
8
9 fizz
10 buzz
11
12 fizz
13
14 sezz
15 fizz buzz
16
17
18 fizz
19
20 buzz
21 fizz sezz`
describe("FizzBuzz", ()=>{
  test_equal("fizz_buzz_3_5 1~15",
    fizz_buzz_3_5(~end=15), expected_3_5_to_15)

  test_equal("fizz_buzz_3_5_7 1~21",
    fizz_buzz_sezz(~end=21), expected_3_5_7_to_21)
})
