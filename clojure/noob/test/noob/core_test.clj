(ns noob.core-test
  (:require [clojure.test :refer :all]
            [noob.core :refer :all]))

(deftest a-test
  (testing "I will PASS."
    (is (= 1 1))))

(deftest calculate_fuel_test
  (testing "For a mass of 1969, the fuel required is 654"
    (is (= 654 (calculate_fuel 1969))))
  (testing "For a mass of 0, the fuel required is 0, not -2"
    (is (= 0 (calculate_fuel -2)))))

(deftest calc_fuel_rec_test
  (def result (calc_fuel_rec [] 100756))
  (testing "결과는 [33583 11192 3728 1240 411 135 43 12 2 0] 이다"
    (is (= [33583 11192 3728 1240 411 135 43 12 2 0] result)))
  (testing "총 합은 50346 이다"
    (is (= 50346 (reduce + result)))))
