open Js

type jolts = array<int>

let parse_jolts = (input: string): jolts
  => input
    -> String2.trim
    -> String2.split("\n")
    -> Belt.Array.map((line) => line -> Belt.Int.fromString -> Belt.Option.getExn)
    -> Belt.SortArray.Int.stableSort
    -> l => [0] -> Array2.concat(l)

type diff_of_1_2_3 = (int, int, int)

let find_longest_chain = (l: jolts): diff_of_1_2_3
  => l
    -> Array2.reducei(((first, second, third, connect), n, index)=>{
      let next = if index + 1 < l -> Array2.length {
        l -> Js.Array2.unsafe_get(index + 1)
      } else {
        n + 3
      }

      switch next - n {
        | 1 => (first + connect, second, third, connect)
        | 2 => (first, second + connect, third, connect)
        | 3 => (first, second, third + connect, connect)
        | _ => raise(Failure(n -> Belt.Int.toString ++ " " ++ next -> Belt.Int.toString))
      }
    }, (0,0,0, 1))
    -> ((first, second, third, _)) => (first, second, third)

let multifly_1_and_3 = ((first: int, _, third: int)): int
  => first * third
