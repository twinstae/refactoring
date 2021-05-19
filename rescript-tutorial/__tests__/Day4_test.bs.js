// Generated by ReScript, PLEASE EDIT WITH CARE
'use strict';

var Day4 = require("../src/Day4.bs.js");
var Jest = require("@glennsl/bs-jest/src/jest.bs.js");
var Curry = require("bs-platform/lib/js/curry.js");

function testEqual(name, lhs, rhs) {
  return Jest.test(name, (function (param) {
                return Jest.Expect.toEqual(rhs, Jest.Expect.expect(lhs));
              }));
}

function testTrue(name, actual) {
  return testEqual(name, actual, true);
}

function testFalse(name, actual) {
  return testEqual(name, actual, false);
}

Jest.describe("check_height", (function (param) {
        testEqual("193cm <= 193 => valid", Day4.check_height("193cm"), true);
        testEqual("194cm >  193 must less than 193in => invalid", Day4.check_height("194cm"), false);
        testEqual("77in  >  76  must less than 76in => invalid", Day4.check_height("77in"), false);
        testEqual("76in  <= 76  => valid", Day4.check_height("76in"), true);
        return testEqual("190   must ends_with cm or in => invalid", Day4.check_height("190"), false);
      }));

var test_raw = "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\nbyr:1937 iyr:2017 cid:147 hgt:183cm\n\niyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\nhcl:#cfa07d byr:1929\n\nhcl:#ae17e1 iyr:2013\neyr:2024\necl:brn pid:760753108 byr:1931\nhgt:179cm\n\nhcl:#cfa07d eyr:2025 pid:166559648\niyr:2011 ecl:brn hgt:59in";

function test_and_next(v, name, expected, get_actual) {
  testEqual(name, Curry._1(get_actual, v), expected);
  return v;
}

Jest.describe("day4", (function (param) {
        var test_result = test_and_next(test_raw.split("\n\n").map(Day4.get_item_arr), "raw length = 4", 4, (function (v) {
                  return v.length;
                })).map(Day4.check_has_required_fields);
        return testEqual("only two passports are valid", test_result, [
                    true,
                    false,
                    true,
                    false
                  ]);
      }));

exports.testEqual = testEqual;
exports.testTrue = testTrue;
exports.testFalse = testFalse;
exports.test_raw = test_raw;
exports.test_and_next = test_and_next;
/*  Not a pure module */
