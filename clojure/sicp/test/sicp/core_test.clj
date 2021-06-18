(ns sicp.core-test
  (:require [clojure.test :refer :all]
            [sicp.core :refer :all]))

(deftest Exercise_1_4
  (testing "a에 b의 절댓값을 더한다."
    (is (= (a-plus-abs-b 3 -3) 6))))

