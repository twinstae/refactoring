open Js

type operation = [#accumulate | #jump | #no_operation]
type instruction = (operation, int)

let to_instruction = (~raw_op: string, ~raw_n: string): instruction => {
  let operation = switch raw_op {
    | "nop" => #no_operation
    | "jmp" => #jump
    | "acc" => #accumulate
    | _ => raise(Failure(`operation 입력이 잘못되었습니다` ++ raw_op))
  }
  let n = switch raw_n -> String2.replace("+", "") -> Belt.Int.fromString {
    | Some(result) => result
    | None => raise(Failure(`입력의 오른쪽 부분을 정수로 변환하지 못했습니다.` ++ raw_n))
  }

  (operation, n)
}

let parse_instruction = (input: string): instruction
  => switch input -> String2.split(" ") {
      | [raw_op, raw_n] => to_instruction(~raw_op=raw_op, ~raw_n=raw_n)
      | _ => raise(Failure(`instruction 입력이 잘못되었습니다.` ++ input))
    }

let parse_instructions = (input: string): array<instruction>
  => input
    -> String2.trim
    -> String2.split("\n")
    -> Array2.map(parse_instruction)

let execute = (inst: instruction, now: int, acc: int): (int, int)
  => switch inst {
    | (#no_operation, _) => (now + 1, acc)
    | (#accumulate, v) => (now + 1, acc + v)
    | (#jump, v) => (now + v, acc)
  }

let rec stop_until_loop = (
  ~now: int = 0,
  ~acc: int = 0,
  ~visited: array<int> = [],
  instructions: array<instruction>
): int
  => if visited -> Array2.includes(now) {
    switch visited -> Array2.pop {
      | Some(_) => acc
      | None => raise(Failure(`visited가 비어있다니 어떻게 이럴 수가!`))
    }
  } else {
    let (next, new_acc) = switch instructions -> Belt.Array.get(now) {
      | Some(v) => v -> execute(now, acc)
      | None => raise(Failure(`index가 범위를 벗어났습니다.` ++ visited -> Array2.toString))
    }
    stop_until_loop(
      instructions,
      ~now=next,
      ~acc=new_acc,
      ~visited=visited -> Array2.concat([now]))
  }

type ending = [#loop | #success]

open Belt
let correct_and_run = (instructions: array<instruction>): int
  => {
    let last_index = instructions -> Array2.length - 1

    let rec dfs = (
      ~fixed: bool,
      ~visited: Set.Int.t,
      (now: int, acc: int)
    ): (int, ending)
    => {     
      let to_the_end = (item: instruction, new_fixed: bool) =>
         item -> execute(now, acc) -> dfs(~fixed=new_fixed, ~visited=visited -> Set.Int.add(now))

      let left_or_right = () => {
        let (left_op, delta) = instructions -> Array2.unsafe_get(now) 
        let (left_acc, left_ending) = (left_op, delta) -> to_the_end(fixed)

        if (fixed || left_op == #accumulate || left_ending == #success){
          (left_acc, left_ending)
        } else { // no_op or jump, not fixed, left failed
          let right_op = left_op == #no_operation ? #jump : #no_operation
          (right_op, delta) -> to_the_end(true)
        }
      }

      let is_visited = visited -> Set.Int.has(now)
      let is_last = now == last_index

      switch (is_visited, is_last) {
        | (true, _) => (acc, #loop)
        | (false, true) => {
          let (_, last_acc) = instructions -> Array2.unsafe_get(last_index) -> execute(now, acc)
          (last_acc, #success)
        }
        | (false, false) => left_or_right()
      }
    }

    switch (0,0) -> dfs(~fixed=false, ~visited=Belt.Set.Int.empty) {
      | (acc, #success) => acc
      | (_, #loop) => raise(Failure("답을 찾지 못했습니다."))
    }
  }
