(ns sicp.core
  (:gen-class))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))

(defn a-plus-abs-b [a b]
  ((if (> b 0) + -) a b))

(defn average [x y]
  (/ (+ x y) 2))

(defn improve [guess x]
  (average guess (/ x guess)))

(defn abs [v]
  (if (>= v 0) v (- v)))

(defn square [x]
  (* x x))

(defn square-sum [x y] (+ (square x) (square y)))

(defn largest-two-square-sum [x y z]
  (cond (and (>= x z) (>= y z)) (square-sum x y)
        (and (>= x y) (>= z y)) (square-sum x z)
        :else (square-sum y z)))

(defn good-enough? [guess x]
  (< (abs (- (square guess) x)) 0.001))

(good-enough? 1.41421356237 2)

(defn sqrt-iter [guess x]
  (if (good-enough? guess x)
    guess
    (sqrt-iter (improve guess x)
               x)))

(defn sqrt [x]
  (sqrt-iter 1.0 x))

(sqrt 2)

(defn factorial [n]
  (if (= n 1)
    1
    (* n (factorial (- n 1)))))

(factorial 3)

(defn fact-iter [product counter max-count]
  (if (> counter max-count)
    product
    (fact-iter (* counter product)
               (+ counter 1)
               max-count)))

(defn factorial2 [n]
  (fact-iter 1 1 n))

(factorial2 3)

(defn A [x y]
  (cond
    (= y 0) 0
    (= x 0) (* 2 y)
    (= y 1) 2
    :else (A (- x 1) (A x (- y 1)))))

;;; test

(defn cube [x]
  (* x x x))

(defn cube-root [x]
  (defn improve
    [guess]
    (average guess (/ (+ (/ x (square guess))(* 2 guess)) 3)))
  (defn good-enough?
    [guess]
    (< (abs (- (cube guess) x)) 0.000001))
  (defn cube-iter
    [guess]
    (if (good-enough? guess)
      guess
      (cube-iter (improve guess))))
  (cube-iter 1.0))

(cube-root 27)
(cube-root 8)
(cube-root 2)

(defn first-denomination [kinds-of-coins]
  (cond
    (= kinds-of-coins 1) 1 
    (= kinds-of-coins 2) 5
    (= kinds-of-coins 3) 10
    (= kinds-of-coins 4) 25
    (= kinds-of-coins 5) 50))

(defn cc [amount kinds-of-coins]
  (cond
    (= amount 0) 1
    (or (< amount 0) (= kinds-of-coins 0)) 0
    :else (+ (cc amount
                 (- kinds-of-coins 1))
             (cc (- amount (first-denomination kinds-of-coins))
                 kinds-of-coins))))

(defn count-change [amount]
  (cc amount 5))

(defn f-iter [[a b c] now-n target-n]
  (cond
    (= now-n target-n) c
    :else
      (f-iter
        [ b c (+ c (* 2 b) (* 3 a)) ]
        (+ now-n 1)
        target-n)))

(defn f [n]
  (cond
    (< n 3) n
    :else (f-iter [1 2 4] 3 n)))

(defn next-line [above]
  (map + (concat above [0]) (concat [0] above)))

(defn pascal [n]
  (if (= n 1) [1] (next-line (pascal (- n 1)))))

(defn fast-expt [b n]
  (cond (= n 0) 1
        (even? n) (square (fast-expt b (/ n 2)))
        :else (* b (fast-expt b (- n 1)))))

(defn double-by-plus [n]
  (+ n n))

(defn multiply-int [a b]
  (cond (= b 1) a
        (even? b) (double-by-plus (multiply-int a (/ b 2)))
        :else (+ a (multiply-int a (- b 1)))))
