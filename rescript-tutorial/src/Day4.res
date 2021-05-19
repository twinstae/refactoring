let test_raw = `ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in`

type key = [
  #birth_year | #issue_year | #expiration_year |
  #height | #hair_color | #eye_color |
  #passport_id | #country_id
]

type item = (key, string)

let str_to_key = (str: string)
  => switch str {
    | "byr" => #birth_year
    | "iyr" => #issue_year
    | "eyr" => #expiration_year
    | "hgt" => #height
    | "hcl" => #hair_color
    | "ecl" => #eye_color
    | "pid" => #passport_id
    | "cid" => #country_id
    | invalid_key => raise(Failure("invalid str key"++invalid_key))
  }

let get_item_arr = (raw_p: string): array<item>
  => raw_p
    -> Js.String2.replaceByRe(%re("/\\n/g"), " ")
    -> Js.String2.split(" ")
    -> Js.Array2.map(raw_item => raw_item -> Js.String2.split(":"))
    -> Js.Array2.map(v => switch v {
      | [k, v] => (str_to_key(k), v)
      | _ => raise(Failure("not valid key value pair"))
    })

let log_and_next = (a) => {
  Js.log(a)
  a
}

let check_has_required_fields = (item_arr: array<item>): bool => {
    let key_arr = item_arr -> Js.Array2.map(((k, _))=> k)
    [
      #birth_year, #issue_year, #expiration_year,
      #height, #hair_color, #eye_color,
      #passport_id
    ]// "cid"
      -> Js.Array2.every(k => key_arr -> Js.Array2.includes(k))
  }

let in_range = (v: string, from_, to_): bool => {
  let option_int_v = Belt.Int.fromString(v)
  switch option_int_v {
    | Some(int_v) => from_ <= int_v && int_v <= to_
    | None => false
  }
}

let check_height = (h: string): bool => {
  switch Js.String2.match_(h, %re("/^([0-9]{2,3})(cm|in)$/")) {
    | Some([_, v, "cm"]) => v -> in_range(150, 193)
    | Some([_, v, "in"]) => v -> in_range(59, 76)
    | Some(_) => false
    | None => false
  }
}

let check_re = (v: string, regExp: Js_re.t)
    => switch Js.String2.match_(v, regExp) {
      | Some(_) => true
      | None => false
    }

let eye_color_set = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"] -> Belt.Set.String.fromArray

Js.log2("regex test expect true = ", "#123abc" -> check_re(%re("/^#[0-9a-f]{6}$/")))
Js.log2("regex test expect false = ", "#123abz" -> check_re(%re("/^#[0-9a-f]{6}$/")))

Js.log2("color_test expect false = ", eye_color_set -> Belt.Set.String.has("wat"))
Js.log2("color test expect true = ", eye_color_set -> Belt.Set.String.has("brn"))

Js.log2("in range test expect true = ", "2020" -> in_range(2010, 2020))
Js.log2("in range test expect false = ", "2021" -> in_range(2010, 2020))

Js.log2("check height expect true = ", "193cm" -> check_height)
Js.log2("check height expect false = ", "194cm" -> check_height)
Js.log2("check height expect false = ", "190in" -> check_height)
Js.log2("check height expect true = ", "60in" -> check_height)
Js.log2("check height expect false = ", "190" -> check_height)


let validate_fields = (item_arr: array<item>): bool => {
  item_arr
    -> Js.Array2.every((item)
      => switch item {
        | (#birth_year, v)      => v -> in_range(1920, 2002)
        | (#issue_year, v)      => v -> in_range(2010, 2020)
        | (#expiration_year, v) => v -> in_range(2020, 2030)
        | (#height, v)          => v -> check_height
        | (#hair_color, v)      => v -> check_re(%re("/^#[0-9a-f]{6}$/"))
        | (#eye_color, v)       => eye_color_set -> Belt.Set.String.has(v)
        | (#passport_id, v)     => v -> check_re(%re("/^[0-9]{9}$/"))
        | (#country_id, _)      => true
      }
    )
}

test_raw
  -> Js.String2.split("\n\n")
  -> Js.Array2.map(get_item_arr)
  -> Js.Array2.filter(check_has_required_fields)
  -> Js.Array2.length
  -> Js.log

Node.Fs.readFileAsUtf8Sync("input/Day4.txt")
  -> Js.String2.trim
  -> Js.String2.split("\n\n")
  -> Js.Array2.map(get_item_arr)
  -> Js.Array2.filter(check_has_required_fields)
  -> Js.Array2.filter(validate_fields)
  -> Js.Array2.length
  -> Js.log
