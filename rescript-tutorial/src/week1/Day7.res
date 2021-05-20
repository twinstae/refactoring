open Js

// type bag = []

type rule = {
  outer: string,
  inner: array<(string, int)>
}

open String2

let parseInt = (v: string)
  => switch v -> Belt.Int.fromString {
      | Some(n) => n
      | None => raise(Failure(v ++ "is not int"))
    }

let parse_inner = v
  => switch v -> match_(%re("/^([0-9]+) ([a-z]+ [a-z]+)/")) {
    | Some([_, count, bag]) => (bag, count -> parseInt)
    | Some(_) => raise(Failure("invalid inner input " ++ v))
    | None => raise(Failure("invalid inner input " ++ v))
  }

let parse_right = (right: string): array<(string, int)> =>
  switch right -> includes("no other") {
    | true => []
    | false => right
      -> replace(".", "")
      -> split(", ")
      -> Array2.map(parse_inner)
  }

let parseRule = (input: string): rule
  => input
    -> replaceByRe(%re("/bags/g"), "")
    -> replaceByRe(%re("/bag/g"), "")
    -> split(" contain ")
    -> v => switch v {
      | [left, right] => {
        outer: left->trim,
        inner: parse_right(right)
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
      r.inner -> Array2.forEach(((inner_bag, _))=>{
        let opt_outer = acc -> Dict.get(inner_bag)
        let old = switch opt_outer {
          | Some(outer_arr) => outer_arr
          | None => []
        }
        acc -> Dict.set(inner_bag, old -> Array2.concat([r.outer]))
      })
      acc
    }, Dict.empty())

type reverse_dict = Dict.t<array<(string, int)>>

let to_reverse_dict = (l: array<rule>): reverse_dict
  => l
    -> Array2.reduce((acc, rule)=> {
        acc -> Dict.set(rule.outer, rule.inner)
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

let rec count_all_inner = (
  d: reverse_dict,
  now_bag: string,
): int => {
  let childs = d -> Dict.get(now_bag)

  switch childs {
    | Some(bag_n_arr)
      => bag_n_arr
        -> Array2.reduce((acc, (bag, n))=>{
          acc + (count_all_inner(d, bag) * n)
        }, 1)
    | None => 1
  }
}
