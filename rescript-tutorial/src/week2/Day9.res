open Js

let parseNumbers = (input: string): array<int>
  => input
    -> String2.trim
    -> String2.split("\n")
    -> Array2.map((line: string) => Belt.Int.fromString(line) -> Belt.Option.getExn)

let find_invalid = (~preamble: int, numbers: array<int>): int
  => {
    let check_invalid = (n: int, i: int): bool 
    => {
      let before_n = numbers -> Array2.slice(~start=i-preamble, ~end_=i)
      before_n
        -> Array2.find((v) => before_n -> Array2.includes(n - v) && n-v != v)
        -> Belt.Option.isNone
    }

    numbers
      -> Array2.findi((n, i) => i < preamble ? false : check_invalid(n,i))
      -> Belt.Option.getExn
  }

let find_contiguous_set = (numbers: array<int>, target: int): array<int>
  => numbers
    -> Array2.reducei((result, _, i) =>{
      if result -> Array2.length > 0 {
        result
      } else {
        let (_, find, index) = numbers
          -> Array2.sliceFrom(i)
          -> Array2.reducei(((sum, find, index), v, j)=>{
            if find {
              (sum, true, index)
            } else {
              (sum + v, sum + v == target, j)
            }
          }, (0, false, 0))
        switch (find, index){
          | (true, index) => numbers -> Array2.slice(~start=i, ~end_=i+index+1)
          | (false, _) => []
        }
      }
    }, [])


let min_max_sum = (l: array<int>) =>{
  let min = l -> Math.minMany_int
  let max = l -> Math.maxMany_int

  min + max
}
