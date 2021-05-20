open Js
open Belt
open String2

let get_group_list = (input: string)
  => input -> trim -> split("\n\n")

let to_char_array = (str: string): array<string>
  => str -> castToArrayLike -> Array2.from

let all_alpha_lower = "abcdefghijklmnopqrstuvwxyz"
let valid_answer_set = Set.String.fromArray(all_alpha_lower -> to_char_array)

open Set.String
let count_group_unique = (group: string) => {
  group
    -> to_char_array
    -> Array2.filter(v => valid_answer_set->has(v))
    -> Set.String.fromArray
    -> size
}

let count_every_person = (group: string): int => {
  group
    -> String2.split("\n")
    -> Array2.map(answer => fromArray(answer -> to_char_array))
    -> Array2.reduce((acc, s)=> intersect(acc, s), valid_answer_set)
    -> size
}
