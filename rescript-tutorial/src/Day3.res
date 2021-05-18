let input_to_tree_map = (raw_input) =>
  raw_input
    -> Js.String.split("\n", _)
    -> Js.Array.map(row=> Js.String.split("", row), _)


let getSize = (map) => (Js.Array.length(map), Js.Array.length(map[0]))
let getRoute = (~down, ~right) => ((height, width))
  => Belt.Array.range(0, height-1)
  -> Js.Array.filter((y)=>mod(y, down) == 0, _)
  -> Js.Array.mapi((y, x)=>(y, mod(x*right, width)), _)


let bool_array_sum = (bool_array) => Js.Array.reduce((acc, v) => acc + (v ? 1 : 0), 0, bool_array)

let count_tree = (~down, ~right)=> (tree_map) => {
  let route = tree_map -> getSize -> getRoute(~down=down, ~right=right)
  let is_tree = ((y, x)) => tree_map[y][x] == "#"

  route
    -> Js.Array.map(is_tree, _)
    -> bool_array_sum
  }

let test_tree = Day3Input.test_input
  -> input_to_tree_map

let test_result = test_tree -> count_tree(~down=1, ~right=3)

Js.Console.log(test_result == 7)

let test_suite = [(1,1), (1,3), (1,5), (1,7), (2, 1)]

test_suite
  -> Js.Array.map(((d, r)) => test_tree -> count_tree(~down=d, ~right=r), _)
  -> v => Js.Console.log(v == [2,7,3,4,2])

let real_tree = Day3Input.raw_input -> input_to_tree_map

let result = real_tree -> count_tree(~down=1, ~right=3)

Js.Console.log(result == 250)

test_suite
  -> Js.Array.map(((d, r)) => real_tree -> count_tree(~down=d, ~right=r), _)
  -> Js.Array.reduce((acc, v) => acc * v, 1, _)
  -> Js.Console.log
