open Jest
open TestUtil
open Day9
let test_input = `35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576`
let test_numbers_expected = [35,20,15,25,47,40,62,55,65,95,102,117,150,182,127,219,299,277,309,576]
let real_input = Node.Fs.readFileAsUtf8Sync("input/Day9.txt")
  -> Js.String2.trim

describe("parseNumbers", ()=>{
  test_equal(`test_input을 넣으면 기대하는 array<int>를 반환한다`,
    test_input -> parseNumbers, test_numbers_expected)

  test_equal(`real_input을 넣으면 반환하는 array의 길이가 1000이다.`,
    real_input -> parseNumbers -> Js.Array2.length, 1000)
})

describe("find_invalid", ()=>{
  test_equal(`[1...25, 50] 에 (preamble=25)로 실행하면 50을 반환한다.`,
    Belt.Array.range(1, 25) -> Js.Array2.concat([50]) -> find_invalid(~preamble=25), 50)

  test_equal(`test_numbers에 (preamble=5)로 실행하면 127을 반환한다`,
    test_input -> parseNumbers -> find_invalid(~preamble=5), 127)

  test_equal(`real_numbers에 (preamble=25)로 실행하면 675280050를 반환한다`,
    real_input -> parseNumbers -> find_invalid(~preamble=25), 675280050)
})

describe("find_contiguous_set", ()=>{
  let test_result = test_input -> parseNumbers -> find_contiguous_set(127);
  
  test_equal(`test_input을 넣고 target=127로 실행하면 [15,25,47,40] 을 반환한다`,
    test_result, [15,25,47,40])

  test_equal(`test_input을 넣고 target=127으로 실행하면 최솟값 최댓값의 합은 67 이다.`,
    test_result -> min_max_sum, 62)

  let real_result = real_input -> parseNumbers -> find_contiguous_set(675280050)

  test_equal(`real_input을 넣고 target=675280050으로 실행하면 최삿값 최댓값의 합은 96081673 이다.`,
    real_result -> min_max_sum, 96081673)
})
