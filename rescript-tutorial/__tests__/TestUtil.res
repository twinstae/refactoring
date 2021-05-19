open Jest
open Expect

type test_equal<'a> = (string, 'a, 'a) => assertion

let test_equal =(name: string, actual: 'a, expected: 'a) =>
  test(name, ()=>expect(actual)|>toEqual(expected))

test_equal("test_equal test 128 + 128 = 256", 128+128, 256)

