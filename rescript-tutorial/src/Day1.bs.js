// Generated by ReScript, PLEASE EDIT WITH CARE
'use strict';

var Fs = require("fs");
var Belt_Int = require("bs-platform/lib/js/belt_Int.js");
var Belt_SetInt = require("bs-platform/lib/js/belt_SetInt.js");

var raw_input = Fs.readFileSync("input/Day1.txt", "utf8");

var input_str_arr = raw_input.split("\n");

function parse_int(str) {
  var option_n = Belt_Int.fromString(str);
  if (option_n !== undefined) {
    return option_n;
  } else {
    return -1;
  }
}

var input_arr = input_str_arr.map(parse_int);

var input_set = Belt_SetInt.fromArray(input_arr);

var result = input_arr.filter(function (n) {
      return Belt_SetInt.has(input_set, 2020 - n | 0);
    });

if (result.length !== 2) {
  console.log(result, "there is more than one answer!");
} else {
  var a = result[0];
  var b = result[1];
  console.log(a, b);
  console.log(Math.imul(a, b));
}

var result3 = input_arr.filter(function (n) {
      var rest_set = Belt_SetInt.remove(input_set, n);
      var rest_arr = Belt_SetInt.toArray(rest_set);
      var rest = 2020 - n | 0;
      var find = rest_arr.filter(function (m) {
            return Belt_SetInt.has(rest_set, rest - m | 0);
          });
      if (find.length !== 2) {
        return false;
      }
      var a = find[0];
      var b = find[1];
      console.log(a, b, n);
      console.log(Math.imul(Math.imul(a, b), n));
      return true;
    });

exports.raw_input = raw_input;
exports.input_str_arr = input_str_arr;
exports.parse_int = parse_int;
exports.input_arr = input_arr;
exports.input_set = input_set;
exports.result = result;
exports.result3 = result3;
/* raw_input Not a pure module */
