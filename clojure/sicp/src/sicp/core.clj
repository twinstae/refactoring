(ns sicp.core
  set syntax=clojure
  (:gen-class))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))

(defn a-plus-abs-b
  [a b]
  ((if (> b 0) + -) a b))

(defn average
  [x y]
  (/ (+ x y) 2))

(defn improve
  [guess x]
  (average guess (/ x guess)))

(defn abs
  [v]
  (if (>= v 0) v (- v)))

(defn square
  [x]
  (* x x))

(defn square-sum [x y] (+ (square x) (square y)))

(defn largest-two-square-sum
  [x y z]
  (cond (and (>= x z) (>= y z)) (square-sum x y)
        (and (>= x y) (>= z y)) (square-sum x z)
        :else (square-sum y z)))

(defn good-enough?
  [guess x]
  (< (abs (- (square guess) x)) 0.001))

(good-enough? 1.41421356237 2)

(defn sqrt-iter
  [guess x]
  (if (good-enough? guess x)
    guess
    (sqrt-iter (improve guess x)
               x)))

(defn sqrt
  [x]
  (sqrt-iter 1.0 x))

(sqrt 2)

(defn factorial
  [n]
  (if (= n 1)
    1
    (* n (factorial (- n 1)))))

(factorial 3)

(defn fact-iter
  [product counter max-count]
  (if (> counter max-count)
    product
    (fact-iter (* counter product)
               (+ counter 1)
               max-count)))

(defn factorial2
  [n]
  (fact-iter 1 1 n))

(factorial2 3)

(defn A
  [x y]
  (cond
    (= y 0) 0
    (= x 0) (* 2 y)
    (= y 1) 2
    :else (A (- x 1) (A x (- y 1)))))
