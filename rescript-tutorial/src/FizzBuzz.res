open Js.Array2

let fizz_buzz_3_5 = (~end: int): string
  => Belt.Array.range(1, end)
    -> map(n =>{
      let right = switch (mod(n, 3) == 0, mod(n, 5) == 0) {
        | (false, false) => ""
        | (true, false) => " fizz"
        | (false, true) => " buzz"
        | (true, true) => " fizz buzz"
      }
      n -> Belt.Int.toString ++ right
    })
    -> joinWith("\n")

let fizz_buzz_sezz = (~end: int): string
  => Belt.Array.range(1, end)
    -> map(n=>{
      let right = [(3, "fizz"), (5, "buzz"), (7, "sezz")]
        -> map(((k, word))=> mod(n, k) == 0 ? (" " ++ word) : "")
        -> joinWith("")
        
      n -> Belt.Int.toString ++ right
    })
    -> joinWith("\n")
