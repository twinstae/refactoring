let input_str_arr: array<string> = Js.String.split("\n", Day1Input.raw_input)

let parse_int = (str: string) => {
  let option_n = Belt.Int.fromString(str)

  switch option_n {
    | Some(n) => n
    | None => -1
  }
}

let input_arr: array<int> = Js.Array.map(parse_int, input_str_arr)
let input_set: Belt.Set.Int.t = Belt.Set.Int.fromArray(input_arr)

let result = input_arr -> Js.Array.filter(n => input_set->Belt.Set.Int.has(2020 - n), _)

switch result {
  | [a, b] => {
    Js.Console.log2(a, b)
    Js.Console.log(a * b)
  }
  | notValid => {
    Js.Console.log2(notValid, "there is more than one answer!")
  }
}

let result3 = input_arr
  -> Js.Array.filter(
    n => {
      let rest_set = input_set-> Belt.Set.Int.remove(n)
      let rest_arr = rest_set -> Belt.Set.Int.toArray
      let rest = 2020 - n
      
      let find = rest_arr -> Js.Array.filter(m => rest_set->Belt.Set.Int.has(rest - m), _)

      switch find {
        | [a, b] => {
          Js.Console.log3(a,b,n)
          Js.Console.log(a*b*n)
          true
        }
        | _ => false
      }
    },
    _
  )
