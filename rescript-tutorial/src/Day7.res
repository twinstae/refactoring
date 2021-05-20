open Js

// type bag = []

type rule = {
  outer: string,
  inner: array<string>
}

open String2

let parse_inner = (right: string): array<string> =>
  right
  -> replace(".", "")
  -> split(", ")
  -> Array2.map(v => v -> replaceByRe(%re("/[0-9]+ /"), "") -> trim)

let parseRule = (input: string): rule
  => input
    -> replaceByRe(%re("/bags/g"), "")
    -> replaceByRe(%re("/bag/g"), "")
    -> split(" contain ")
    -> v => switch v {
      | [left, right] => {
        outer: left->trim,
        inner: parse_inner(right)
      }
      | _ => raise(Failure("invalid rule input" ++ v->Array2.joinWith(" ")))
    }

let parseRules = (input: string): array<rule>
  => input
    -> String2.split("\n")
    -> Array2.map(parseRule)

type rules_dict = Dict.t<array<string>>

let to_dict = (l: array<rule>): rules_dict
  => l
    -> Array2.reduce((acc, r)=>{
      r.inner -> Array2.forEach((inner_bag)=>{
        let opt_outer = acc -> Dict.get(inner_bag)
        let old = switch opt_outer {
          | Some(outer_arr) => outer_arr
          | None => []
        }
        acc -> Dict.set(inner_bag, old -> Array2.concat([r.outer]))
      })
      acc
    }, Dict.empty())

open Belt

let rec how_many = (
  d: rules_dict,
  now_bag: string,
  childs: Set.String.t
): Set.String.t => {
  let childs_with_now = childs -> Set.String.add(now_bag)
  let parents = d -> Dict.get(now_bag)
  
  switch parents {
    | Some(l) => l -> Array2.reduce((acc, parent) =>{
      switch acc -> Set.String.has(parent) {
        | false => how_many(d, parent, acc)
        | true => acc
      }
    }, childs_with_now)
    | None => childs_with_now
  }
}
