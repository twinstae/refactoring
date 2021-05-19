let input_to_tree_map = (raw_input) =>
  raw_input
    -> Js.String2.split("\n")
    -> Js.Array2.map(row => Js.String.split("", row))


let getSize = (map: array<array<string>>): (int, int) => (Js.Array.length(map), Js.Array.length(map[0]))
let getRoute = (~down, ~right) => ((height, width))
  => Belt.Array.range(0, height-1)
  -> Js.Array2.filter((y)=>mod(y, down) == 0)
  -> Js.Array2.mapi((y, x)=>(y, mod(x*right, width)))


let bool_array_sum = ba => ba -> Js.Array2.reduce((acc, v) => acc + (v ? 1 : 0), 0)

let count_tree = (~down, ~right) => (tree_map): int => {
    let route = tree_map -> getSize -> getRoute(~down=down, ~right=right)
    let is_tree = ((y, x)) => tree_map[y][x] == "#"

    route
      -> Js.Array2.map(is_tree)
      -> bool_array_sum
  }

let test_input = `..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#`

let test_tree = test_input
  -> input_to_tree_map

test_tree
  -> count_tree(~down=1, ~right=3)
  -> t => Js.Console.log(t == 7)

let test_suite = [(1,1), (1,3), (1,5), (1,7), (2, 1)]

test_suite
  -> Js.Array2.map(((d, r)) => test_tree -> count_tree(~down=d, ~right=r))
  -> v => Js.Console.log(v == [2,7,3,4,2])

let real_tree = Node.Fs.readFileAsUtf8Sync("input/Day3.txt")
 -> Js.String2.trim
 -> input_to_tree_map

 real_tree
  -> count_tree(~down=1, ~right=3)
  -> r => Js.Console.log(r == 250)

test_suite
  -> Js.Array2.map(((d, r)) => count_tree(~down=d, ~right=r))
  -> Js.Array2.map(f => f(real_tree))
  -> Js.Array2.reduce((acc, v) => acc * v, 1)
  -> Js.Console.log
