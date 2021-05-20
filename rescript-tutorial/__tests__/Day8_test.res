open Jest
open TestUtil
open Day8

let test_input= `nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6`

let expected_instruction: array<instruction> = [
  (#no_operation, 0),
  (#accumulate, 1),
  (#jump, 4),
  (#accumulate, 3),
  (#jump, -3),
  (#accumulate, -99),
  (#accumulate, +1),
  (#jump, -4),
  (#accumulate, +6)
]

describe("Day8 Handheld Halting part1", ()=>{
  describe(`test input으로`, ()=>{
    test_equal(`acc +1 을 parse_instruction 하면 (#accumulate, 1) 을 반환한다.`,
      "acc +1" -> parse_instruction, (#accumulate, 1)
    )

    let test_instructions = test_input -> parse_instructions

    test_equal(`parse_instructions 하면, 올바른 array<instruction>을 반환한다.`,
      test_instructions, expected_instruction)

    test_equal(`stop_until_loop 하면, 마지막 acc 값 5를 반환한다`,
      test_instructions -> stop_until_loop, 5)

    test_equal(`correct_and_run 하면, 마지막 acc 값 8을 반환한다`,
      test_instructions -> correct_and_run, 8)
  })

  describe(`real_input 으로`, ()=>{
    let real_instructions = Node.Fs.readFileAsUtf8Sync("input/Day8.txt")
      -> Js.String2.trim
      -> parse_instructions

    test_equal(`stop_until_loop 하면 마지막 acc 값 1675를 반환한다.`,
      real_instructions-> stop_until_loop, 1675)
    
    test_equal(`correct_and_run 하면 마지막 acc 값 ... 을 반환한다`,
      real_instructions-> correct_and_run, 1532)
  })
})
