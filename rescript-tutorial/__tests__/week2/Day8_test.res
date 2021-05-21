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

let expected_instructions: array<instruction> = [
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

open Js

let toString = (item: instruction): string
  => item -> Json.stringifyAny -> Belt.Option.getExn

describe("Day8 Handheld Halting part1", ()=>{
  describe(`parse_instruction`, ()=>{
    test_each_line(test_input, expected_instructions)(
      (line, expected)=>{
        test_equal(`"${line}"이 들어오면 ${expected->toString} 을 반환한다.`,
          line -> parse_instruction, expected)})

    test_equal(`parse_instructions를 test_input에 적용하면, 올바른 array<instruction>을 반환한다.`,
      test_input -> parse_instructions, expected_instructions)
  })

  let test_instructions = test_input -> parse_instructions
  let real_instructions = Node.Fs.readFileAsUtf8Sync("input/Day8.txt")
    -> Js.String2.trim
    -> parse_instructions

  describe(`stop_until_loop를`, ()=>{
    test_equal(`test_instructions에 적용하면, 마지막 acc 값 5를 반환한다`,
      test_instructions -> stop_until_loop, 5)

    test_equal(`real_instructions에 적용하면 마지막 acc 값 1675를 반환한다.`,
      real_instructions-> stop_until_loop, 1675)
  })
  describe(`correct_and_run을`, ()=>{
    test_equal(`test_instructions에 적용하면, 마지막 acc 값 8을 반환한다`,
      test_instructions -> correct_and_run, 8)   
    test_equal(`real_instructions에 적용하면 마지막 acc 값 1532를 반환한다`,
      real_instructions-> correct_and_run, 1532)
  })
})
