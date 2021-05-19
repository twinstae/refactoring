open Jest
open TestUtil

type color = [ #red | #blue | #green ]

module ColorCmp = Belt.Id.MakeComparable({
  type t = color
  let cmp = Pervasives.compare
})

describe("variant set", ()=>{
  open Belt
  let red_blue_set = Set.fromArray([#red, #blue], ~id=module(ColorCmp))
  
  test_equal("red_blue_set has red", red_blue_set -> Set.has(#red), true)

  test_equal("red_blue_set has not greed", red_blue_set -> Set.has(#green), false)
})

let test_input = `abc

a
b
c

ab
ac

a
a
a
a

b`

describe("Day 6 Custom Customs", ()=>{
  open Js.Array2

  let test_group_list = Day6.get_group_list(test_input)
  test_equal("test group length is 5", test_group_list->length, 5)
  
  test_equal("test result is [3,3,3,1,1]",
    test_group_list-> map(Day6.count_group_unique), [3,3,3,1,1])

  let group_list = Node.Fs.readFileAsUtf8Sync("input/Day6.txt") -> Day6.get_group_list

  let sum_of_count = group_list
    -> map(Day6.count_group_unique)
    -> reduce((acc, v) => acc+v, 0)

  test_equal("sum of counts is ...", sum_of_count, 6387)

  test_equal("all answered yes questions in test_input is [3,0,1,1,1]",
    test_group_list -> map(Day6.count_every_person), [3,0,1,1,1]
  )

  let sum_of_count_2 = group_list
    -> map(Day6.count_every_person)
    -> reduce((acc,v)=>acc+v, 0)

  test_equal("all answered yes questions's sum is 3038",
    sum_of_count_2, 3039
  )
})

