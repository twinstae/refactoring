(ns noob.core
  (:gen-class))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World"))

(require '[clojure.edn :as edn])
(defn parse_mass
  [input]
  (edn/read-string input))

(defn calculate_fuel
  "divide by three, round down, and subtract 2"
  [mass]
  (-> mass (/ 3) (Math/floor) (int) (- 2) (max 0)))

(defn calc_fuel_rec
  "calculate fuel for the mass and then recursively calculate_fuel for the fuel(=new mass)"
  [acc, mass]
  (def new_fuel (calculate_fuel mass))
  (if (> mass 0) (calc_fuel_rec (conj acc new_fuel) new_fuel) acc))

