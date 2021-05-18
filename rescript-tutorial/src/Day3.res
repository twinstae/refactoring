let input_to_tree_map = (raw_input) =>
  raw_input
    -> Js.String.split("\n", _)
    -> Js.Array.map(row=> Js.String.split("", row), _)


let getSize = (map) => (Js.Array.length(map), Js.Array.length(map[0]))
let getRoute = ((height, width)) => Js.Array.mapi(
      (y, x)=>(y, mod(x*3, width)),
      Belt.Array.range(0, height-1)
    )

let bool_array_sum = (bool_array) => Js.Array.reduce((acc, v) => acc + (v ? 1 : 0), 0, bool_array)

let count_tree = (tree_map) => {
  let route = tree_map -> getSize -> getRoute
  let is_tree = ((y, x)) => tree_map[y][x] == "#"

  route
    -> Js.Array.map(is_tree, _)
    -> bool_array_sum
  }

let test_result = Day3Input.test_input
  -> input_to_tree_map
  -> count_tree 

Js.Console.log(test_result == 7)

let result = Day3Input.raw_input
  -> input_to_tree_map
  -> count_tree

Js.Console.log(result)
