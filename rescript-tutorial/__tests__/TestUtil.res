open Jest
open Expect

type test_equal<'a> = (string, 'a, 'a) => assertion

let test_equal =(name: string, actual: 'a, expected: 'a) =>
  test(name, ()=>expect(actual)|>toEqual(expected))

test_equal("test_equal test 128 + 128 = 256", 128+128, 256)

let test_each_line = (input_string, expected_list)
  => {
    let pair_list = input_string
    -> Js.String2.trim
    -> Js.String2.split("\n")
    -> Belt.Array.zip(expected_list)

    (test_func) => pair_list-> Js.Array2.forEach(((input, expected)) => test_func(input, expected))
  }
