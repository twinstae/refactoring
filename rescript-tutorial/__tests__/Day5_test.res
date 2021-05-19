open Jest
open Expect
open Day5

let raw_seat = "FBFBBFFRLR"
let raw_row =  "FBFBBFF"
let raw_col =  "RLR"

type test_equal<'a> = (string, 'a, 'a) => assertion

let test_equal =(name: string, actual: 'a, expected: 'a) =>
  test(name, ()=>expect(actual)|>toEqual(expected))

describe("parse seat", ()=>{
  test_equal("parse_row return expected row",
    parse_row(raw_row), 44
  )
  test_equal("parse_col return expected col",
    parse_column(raw_col), 5
  )

  let test_seat = parse_seat(raw_seat)
  test_equal("parse seat return expected seat",
    test_seat, {row: 44, col: 5}
  )

  test_equal("get seat id is return expected", 
    test_seat -> get_seat_id, 357
  )

  let seat_id_list = Node.Fs.readFileAsUtf8Sync("input/Day5.txt")
    -> Js.String2.trim
    -> Js.String2.split("\n")
    -> Js.Array2.map(v => v -> parse_seat -> get_seat_id)

  test_equal("max of seat_id_list is 920", Day5.max(seat_id_list), 926)
  test_equal("max of seat_id_list is 920", Day5.min(seat_id_list), 80)

  test_equal("sum_of_arithmetic_seq 1 to 4 is 10", sum_of_arithmetic_seq(1, 4, 1), 10)

  test_equal("sum of [1,2,4] is 7", sum([1,2,4]), 7)

  test_equal("my_seat is 657!", find_my_seat(seat_id_list), 657)
})
