(ns sicp.core-test
  (:require [clojure.test :refer :all]
            [sicp.core :refer :all]))

(deftest ex_1_3
  (testing "largest-two-square-sum 에 1 2 3 을 넣으면 4+9 = 13"
    (is (= (largest-two-square-sum 1 2 3) 13)))
  (testing "largest-two-square-sum 에 5 2 1 을 넣으면 25+4 = 29"
    (is (= (largest-two-square-sum 5 2 1) 29)))
  (testing "largest-two-square-sum 에 3 8 3 을 넣으면 64+9 = 73"
    (is (= (largest-two-square-sum 3 8 3) 73))))

(deftest Exercise_1_4
  (testing "a에 b의 절댓값을 더한다."
    (is (= (a-plus-abs-b 3 -3) 6))))

(defn p [] (p))

(defn test-order
  [x y]
  (if (= x 0) 0 y))

(comment 
  (deftest Exercise_1_5
    (testing "interpreter applicative order test"
      (is (= (test-order 0 (p)) 0)))))

(deftest Ex-counting-change
  (testing "first-denomination"
    (is (= (first-denomination 1) 1))
    (is (= (first-denomination 2) 5))
    (is (= (first-denomination 3) 10))
    (is (= (first-denomination 4) 25))
    (is (= (first-denomination 5) 50)))
  (testing "거스름돈 예제"
    (is (= (count-change 10) 4))
    (is (= (count-change 100) 292))))

(deftest Ex-1.11
  (testing "f 함수"
    (is (= (f 2) 2))
    (is (= (f 3) 4))
    (is (= (f 4) 11))
    (is (= (f 5) 25))))
