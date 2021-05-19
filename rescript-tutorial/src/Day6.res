open Js
open Belt
open String2

let get_group_list = (input: string) => input -> trim -> split("\n\n")

let all_alpha_lower = "abcdefghijklmnopqrstuvwxyz"
let valid_answer_set = Set.String.fromArray(all_alpha_lower -> split(""))

let count_group_unique = (group: string) => {
  group
    -> split("")
    -> Array2.filter(v => valid_answer_set -> Set.String.has(v))
    -> Set.String.fromArray
    -> Set.String.size
}

let count_every_person = (group: string): int => {
  group
    -> split("\n")
    -> Array2.reduce((acc, answer)=> {
      let answer_set = answer -> split("") -> Set.String.fromArray

      acc -> Array2.filter(v=> answer_set -> Set.String.has(v))
    }, all_alpha_lower->split(""))
    -> Array2.length
}
