let boolean_sum = (bool_arr: array<bool>): int => bool_arr -> Js.Array2.reduce((acc, v) => acc + (v ? 1 : 0), 0)

