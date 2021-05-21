let test_input = `16
10
15
5
1
11
7
19
6
12
4`

let larger_test_input = `28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3`

let real_input = Node.Fs.readFileAsUtf8Sync("input/Day10.txt")

open Jest
open TestUtil
open Day10

let test_jolts_expected = [0, 1,4,5,6,7,10,11,12,15,16,19]
let larger_test_jolts = larger_test_input -> parse_jolts

describe("parse_jolts", ()=>{
  test_equal(`test_input을 넣으면 ${test_jolts_expected -> Js.Array2.toString}을 반환한다`,
    test_input -> parse_jolts, test_jolts_expected)

  test_equal(`larger_test_input을 넣으면 길이가 1+31=32개다.`,
    larger_test_jolts -> Belt.Array.length, 32)

  test_equal(`real_input을 넣으면 길이가 1+=개다.`,
    real_input -> parse_jolts -> Belt.Array.length, 115)
})

let test_result_expected = (7, 0, 5)
let larger_test_result = (22, 0, 10)
describe("find_longest_chain", ()=>{
  test_equal(`built_in을 포함한 test_jolts를 넣으면 (7, 0, 5) 를 반환한다.`,
    test_jolts_expected -> find_longest_chain, test_result_expected)

  test_equal(`test_result의 1-jolt diff와 3-jolt를 곱하면 35가 나온다.`,
    test_result_expected -> multifly_1_and_3, 35)

  test_equal(`built_in 포함 larger_test_jolts를 넣으면 (22, 0, 10)을 반환한다.`,
    larger_test_jolts -> find_longest_chain, larger_test_result)

  test_equal(`larget_test_result의 1-jolt diff와 3-jolt를 곱하면 220이 나온다.`,
    larger_test_result -> multifly_1_and_3, 220)

  let real_jolts = real_input -> parse_jolts
  test_equal(`real_jolts의 1-jolt diff와 3-jolt를 곱하면 ...`,
    real_jolts -> find_longest_chain -> multifly_1_and_3, 3000)
})

