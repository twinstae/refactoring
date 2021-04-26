type language = 
  | ReScript
  | Python
  | Rust
  | Lua

let getLabel = (l: language) =>
  switch l {
  | ReScript => "ReScript"
  | Python => "Python"
  | Rust => "Rust"
  | Lua => "Lua"
  }

let rescript = ReScript

Js.log("Hello, " ++ getLabel(rescript))
