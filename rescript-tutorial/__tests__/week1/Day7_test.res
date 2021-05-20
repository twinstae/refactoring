let test_input = `light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.`

let test_input2 = `shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.`

let choco_rule = "mint choco bags contain 1 vanila cheese bag, 2 chocolate brown bags."

open Jest
open TestUtil
open Js
open Day7

describe("Day7 Handy Haversacks", ()=>{
  describe("part1", ()=>{
    describe("context text input", ()=>{
      let test_rules = test_input -> parseRules
      test_equal("there are 9 rules in test input",
        test_rules -> Array2.length, 9)

      test_equal("parseRule with 1, 2",
        parseRule(choco_rule), {
          outer: "mint choco",
          inner: [("vanila cheese", 1), ("chocolate brown", 2)]
        })

      let test_rules_dict = test_rules -> to_dict
      test_equal("get inner 1 return expected outer",
        test_rules_dict -> Dict.unsafeGet("shiny gold"), ["bright white", "muted yellow"])

      test_equal("get inner 2 return expected outer",
        test_rules_dict -> Dict.unsafeGet("bright white"), ["light red", "dark orange"])

      test_equal("get inner 3 return expected outer",
        test_rules_dict -> Dict.unsafeGet("muted yellow"), ["light red", "dark orange"])

      let test_result = Day7.how_many(test_rules_dict, "shiny gold", Belt.Set.String.empty)
      test_equal("4 bags can contain shing gold bag",
        test_result -> Belt.Set.String.remove("shiny gold") -> Belt.Set.String.toArray,
        ["bright white", "dark orange", "light red", "muted yellow"])
    })
    describe("context: real input", ()=>{
      let real_result = Node.Fs.readFileAsUtf8Sync("input/Day7.txt")
        -> String2.trim
        -> parseRules
        -> to_dict
        -> Day7.how_many("shiny gold", Belt.Set.String.empty)

      test_equal("the number of bags which can contain shiny gold bag is 278",
        real_result -> Belt.Set.String.size - 1, 278)
    })
  })

  describe("part2", ()=>{
    describe("context: in test input 2", ()=>{
      let test_reverse_dict = test_input2 -> parseRules -> to_reverse_dict

      test_equal("reverse_dict get shiny gold return (dark red, 2)",
        test_reverse_dict -> Dict.unsafeGet("shiny gold"), [("dark red", 2)]
      )

      test_equal("in shiny gold bag, there are 126 other bags",
        test_reverse_dict -> count_all_inner("shiny gold") - 1, 126)
    })     
    describe("context: in real input", ()=>{
      let real_result = Node.Fs.readFileAsUtf8Sync("input/Day7.txt")
        -> String2.trim
        -> parseRules
        -> to_reverse_dict
        -> count_all_inner("shiny gold")
      test_equal("in shiny gold bag, there are 1024 other bags",
        real_result - 1, 45157)
    })
  })
})

