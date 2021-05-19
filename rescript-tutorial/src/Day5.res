type seat = {
  row: int,   // 0 ~ 127
  col: int // 0 ~ 7
}
      
let parse_row = (raw: string): int
  => raw
      -> Js.String2.split("")
      -> Js.Array2.reduce((acc, v)=>{
        switch v {
          | "F" => acc * 2 + 0
          | "B" => acc * 2 + 1
          | _ => raise(Failure("invalid row character"))
        }
      }, 0)

let parse_column = (raw: string): int
  => {
    raw
      -> Js.String2.split("")
      -> Js.Array2.reduce((acc, v)=>{
        switch v {
          | "L" => acc * 2 + 0
          | "R" => acc * 2 + 1
          | _ => raise(Failure("invalid row character"))
        }
      }, 0)
  }

let parse_seat = (raw: string): seat
  => {
      row: raw -> Js.String2.slice(~from=0, ~to_=7)-> parse_row,
      col: raw -> Js.String2.sliceToEnd(~from=7)   -> parse_column
    }

let get_seat_id = (s: seat): int => s.row * 8 + s.col

let max = (l: array<int>) => 
  l -> Js.Array2.reduce((max, v) => v > max ? v : max, 0)

let min = (l: array<int>) =>
  l -> Js.Array2.reduce((min, v) => v < min ? v : min, 2048)

let sum_of_arithmetic_seq = (l: array<int>): int
  => (min(l) + max(l)) * (l -> Js.Array2.length) / 2

let sum = (l: array<int>): int
  => l -> Js.Array2.reduce((acc, v) => acc + v, 0)

let find_my_seat = (l: array<int>): int
  => sum_of_arithmetic_seq(l) - sum(l)
