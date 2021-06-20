(ns sicp.core-test
  (:require [clojure.test :refer :all]
            [sicp.core :refer :all]))

(deftest Exercise_1_4
  (testing "a에 b의 절댓값을 더한다."
    (is (= (a-plus-abs-b 3 -3) 6))))

(deftest ex_1_3
  (testing "largest-two-square-sum 에 1 2 3 을 넣으면 4+9 = 13"
    (is (= (largest-two-square-sum 1 2 3) 13)))
  (testing "largest-two-square-sum 에 5 2 1 을 넣으면 25+4 = 29"
    (is (= (largest-two-square-sum 5 2 1) 29)))
  (testing "largest-two-square-sum 에 3 8 3 을 넣으면 64+9 = 73"
    (is (= (largest-two-square-sum 3 8 3) 73))))
