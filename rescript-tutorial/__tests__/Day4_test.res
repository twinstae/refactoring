open Jest
open Expect
open Day4

let testEqual = (name, lhs, rhs) => test(name, () => expect(lhs) |> toEqual(rhs))
let testTrue = (name, actual) => testEqual(name, actual, true)
let testFalse = (name, actual) => testEqual(name, actual, false)

describe("check_height", ()=>{
  testTrue( "193cm <= 193 => valid", "193cm" -> check_height)
  testFalse("194cm >  193 must less than 193in => invalid", "194cm" -> check_height)
  testFalse("77in  >  76  must less than 76in => invalid", "77in" ->  check_height)
  testTrue( "76in  <= 76  => valid", "76in" ->  check_height)
  testFalse("190   must ends_with cm or in => invalid", "190" -> check_height)
})


let test_raw = `ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in`

let test_and_next = (v, name, expected, get_actual) => {
  testEqual(name, get_actual(v), expected)
  v
}

describe("day4", ()=>{
  let test_result = test_raw
    -> Js.String2.split("\n\n")
    -> Js.Array2.map(get_item_arr)
    -> test_and_next("raw length = 4", 4, (v) => v->Js.Array2.length)
    -> Js.Array2.map(check_has_required_fields)
  testEqual("only two passports are valid", test_result, [true, false, true, false])
})
/*
Js.log2("regex test expect true = ", "#123abc" -> check_re(%re("/^#[0-9a-f]{6}$/")))
Js.log2("regex test expect false = ", "#123abz" -> check_re(%re("/^#[0-9a-f]{6}$/")))

Js.log2("color_test expect false = ", eye_color_set -> Belt.Set.String.has("wat"))
Js.log2("color test expect true = ", eye_color_set -> Belt.Set.String.has("brn"))

Js.log2("in range test expect true = ", "2020" -> in_range(2010, 2020))
Js.log2("in range test expect false = ", "2021" -> in_range(2010, 2020))
*/
