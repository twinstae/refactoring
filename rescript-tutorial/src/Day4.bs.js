// Generated by ReScript, PLEASE EDIT WITH CARE
'use strict';

var Fs = require("fs");
var Belt_Int = require("bs-platform/lib/js/belt_Int.js");
var Belt_SetString = require("bs-platform/lib/js/belt_SetString.js");

function str_to_key(str) {
  switch (str) {
    case "byr" :
        return "birth_year";
    case "cid" :
        return "country_id";
    case "ecl" :
        return "eye_color";
    case "eyr" :
        return "expiration_year";
    case "hcl" :
        return "hair_color";
    case "hgt" :
        return "height";
    case "iyr" :
        return "issue_year";
    case "pid" :
        return "passport_id";
    default:
      throw {
            RE_EXN_ID: "Failure",
            _1: "invalid str key" + str,
            Error: new Error()
          };
  }
}

function get_item_arr(raw_p) {
  return raw_p.replace(/\n/g, " ").split(" ").map(function (raw_item) {
                return raw_item.split(":");
              }).map(function (v) {
              if (v.length !== 2) {
                throw {
                      RE_EXN_ID: "Failure",
                      _1: "not valid key value pair",
                      Error: new Error()
                    };
              }
              var k = v[0];
              var v$1 = v[1];
              return [
                      str_to_key(k),
                      v$1
                    ];
            });
}

function log_and_next(a) {
  console.log(a);
  return a;
}

function check_has_required_fields(item_arr) {
  var key_arr = item_arr.map(function (param) {
        return param[0];
      });
  return [
            "birth_year",
            "issue_year",
            "expiration_year",
            "height",
            "hair_color",
            "eye_color",
            "passport_id"
          ].every(function (k) {
              return key_arr.includes(k);
            });
}

function in_range(v, from_, to_) {
  var option_int_v = Belt_Int.fromString(v);
  if (option_int_v !== undefined && from_ <= option_int_v) {
    return option_int_v <= to_;
  } else {
    return false;
  }
}

function check_height(h) {
  var match = h.match(/^([0-9]{2,3})(cm|in)$/);
  if (match === null) {
    return false;
  }
  if (match.length !== 3) {
    return false;
  }
  var v = match[1];
  var match$1 = match[2];
  switch (match$1) {
    case "cm" :
        return in_range(v, 150, 193);
    case "in" :
        return in_range(v, 59, 76);
    default:
      return false;
  }
}

function check_re(v, regExp) {
  var match = v.match(regExp);
  return match !== null;
}

var eye_color_set = Belt_SetString.fromArray([
      "amb",
      "blu",
      "brn",
      "gry",
      "grn",
      "hzl",
      "oth"
    ]);

function validate_fields(item_arr) {
  return item_arr.every(function (item) {
              var match = item[0];
              if (match === "expiration_year") {
                return in_range(item[1], 2020, 2030);
              } else if (match === "eye_color") {
                return Belt_SetString.has(eye_color_set, item[1]);
              } else if (match === "height") {
                return check_height(item[1]);
              } else if (match === "birth_year") {
                return in_range(item[1], 1920, 2002);
              } else if (match === "country_id") {
                return true;
              } else if (match === "passport_id") {
                return check_re(item[1], /^[0-9]{9}$/);
              } else if (match === "issue_year") {
                return in_range(item[1], 2010, 2020);
              } else {
                return check_re(item[1], /^#[0-9a-f]{6}$/);
              }
            });
}

var result = Fs.readFileSync("input/Day4.txt", "utf8").trim().split("\n\n").map(get_item_arr).filter(check_has_required_fields).filter(validate_fields).length;

exports.str_to_key = str_to_key;
exports.get_item_arr = get_item_arr;
exports.log_and_next = log_and_next;
exports.check_has_required_fields = check_has_required_fields;
exports.in_range = in_range;
exports.check_height = check_height;
exports.check_re = check_re;
exports.eye_color_set = eye_color_set;
exports.validate_fields = validate_fields;
exports.result = result;
/* eye_color_set Not a pure module */