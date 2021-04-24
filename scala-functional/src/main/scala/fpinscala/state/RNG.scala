package Ch6

import Ch6.Candy.simulateMachine

import scala.annotation.tailrec

trait RNG {
  def nextInt: (Int, RNG)
}

object RNG {
  case class SimpleRNG(seed: Long) extends RNG {
    def nextInt: (Int, RNG) = {
      val newSeed = (seed * 0x5DEECE66DL + 0xBL) & 0xFFFFFFFFFFFFL
      val nextRNG = SimpleRNG(newSeed)
      val n = (newSeed >>> 16).toInt
      (n, nextRNG)
    }
  }
  def nonNegativeInt(rng: RNG): (Int, RNG) = {
    val (raw_n, nextRNG) = rng.nextInt
    (if (raw_n < 0) -(raw_n + 1) else  raw_n, nextRNG)
  }

  def double(rng: RNG): (Double, RNG) = {
    val (i, r) = nonNegativeInt(rng)
    (i / (Int.MaxValue.toDouble + 1), r)
  }

  def intDouble(rng: RNG): ((Int, Double), RNG) = {
    val (n, nextRNG) = rng.nextInt
    val (d, nextRNG2) = double(nextRNG)

    ((n, d), nextRNG2)
  }
  def doubleInt(rng: RNG): ((Double, Int), RNG) = {
    val (d, nextRNG) = double(rng)
    val (n, nextRNG2) = nextRNG.nextInt

    ((d, n), nextRNG2)
  }
  def double3(rng: RNG): ((Double,Double,Double), RNG) = {
    val (d1, nextRNG) = double(rng)
    val (d2, nextRNG2) = double(nextRNG)
    val (d3, nextRNG3) = double(nextRNG2)

    ((d1, d2, d3), nextRNG3)
  }

  def ints(count: Int)(rng: RNG): (List[Int], RNG) = {
    @tailrec
    def go(count: Int, r: RNG, xs: List[Int]): (List[Int], RNG) =
      if (count == 0)
        (xs, r)
      else {
        val (x, r2) = r.nextInt
        go(count - 1, r2, x :: xs)
      }
    go(count, rng, List())
  }

  type Rand[+A] = RNG => (A, RNG)

  val int: Rand[Int] = _.nextInt

  def unit[A](a: A): Rand[A] =
    rng => (a, rng)

  def map[A,B](s: Rand[A])(f: A => B): Rand[B] =
    rng => {
      val (a, rng2) = s(rng)
      (f(a), rng2)
    }

  val _double: Rand[Double] =
    map(nonNegativeInt)(_ / (Int.MaxValue.toDouble + 1))

  def map2[A,B,C](ra: Rand[A], rb: Rand[B])(f: (A,B) => C): Rand[C] =
    rng => {
      val (a, r1) = ra(rng)
      val (b, r2) = rb(r1)
      (f(a,b), r2)
    }

  def both[A,B](ra: Rand[A], rb: Rand[B]): Rand[(A,B)] =
    map2(ra, rb)((_, _))

  val randDoubleInt: Rand[(Double, Int)] =
    both(_double, int)

  val randIntDouble: Rand[(Int, Double)] =
    both(int, _double)

  def sequence[A](fs: List[Rand[A]]): Rand[List[A]] =
    flatMap(
      fs.foldLeft(unit(List[A]()))
      ((acc, f) => map2(f, acc)(_ :: _))
    )(result=>unit(result.reverse))

  def _ints(count: Int): Rand[List[Int]] =
    sequence(List.fill(count)(int))

  def flatMap[A,B](f: Rand[A])(g: A => Rand[B]): Rand[B] =
    rng => {
      val (a, r1) = f(rng)
      g(a)(r1)
    }

  def nonNegativeLessThan(n: Int): Rand[Int] =
    flatMap(nonNegativeInt)(i=> {
      val mod = i % n
      if (i + (n-1) - mod >= 0) // 오버 플로우가 일어나지 않았다면
        unit(mod)
      else nonNegativeLessThan(n)
    })

  def _map[A,B](s: Rand[A])(f: A => B): Rand[B] = {
    flatMap(s)(a=>unit(f(a)))
  }

  def _map2[A,B,C](ra: Rand[A], rb: Rand[B])(f: (A, B) => C): Rand[C] =
    flatMap(ra)(a => _map(rb)(b => f(a,b)))

  def assertEqual[T](actual: T, expected: T, passMsg: String=""): Unit = {
    val message = s"\n expected: $expected\n actual  : $actual"
    assert(expected == actual, message)
    println("PASS! "+passMsg)
  }

  def rollDie: Rand[Int] = _map(nonNegativeLessThan(6))(_+1)

  def main(args: Array[String]): Unit = {
    val rng = SimpleRNG(42)
    val (n2, rng2) = rng.nextInt
    assertEqual((n2, rng2), (16159453, SimpleRNG(1059025964525L)))
    val (n3, rng3) = rng2.nextInt
    assertEqual((n3, rng3), (-1281479697, SimpleRNG(197491923327988L)))

    // 6.1
    val (n4, _) = nonNegativeInt(rng2)
    assertEqual(n4, 1281479696)

    // 6.2
    val (d, _) = double(rng2)
    assertEqual(d, 0.5967354848980904)

    // 6.3
    val ((n5, d2), _) = intDouble(rng2)
    assertEqual((n5, d2), (-1281479697,0.15846728393808007))
    val ((d3, n6), _) = doubleInt(rng2)
    assertEqual((d3, n6), (0.5967354848980904,-340305902))
    val ((d4, d5, d6), _) = double3(rng2)
    assertEqual((d4, d5, d6), (0.5967354848980904,0.15846728393808007,0.9386595427058637))

    //6.4
    val (n_list, _) = ints(3)(rng2)
    assertEqual(n_list, List(-2015756020, -340305902, -1281479697),
      "ints 는 무작위 정수 n개 리스트를 반환한다")

    //6.5
    assertEqual(_double(rng2), double(rng2),
      "map 으로 만든 _double 은 double 과 같은 결과를 반환한다")

    //6.6
    assertEqual(randIntDouble(rng2), intDouble(rng2),
      "map2로 만든 randIntDouble 는 intDouble 과 같은 결과를 반환한다")

    assertEqual(randDoubleInt(rng2), doubleInt(rng2),
      "map2로 만든 randDoubleInt 는 doubleInt 와 같은 결과를 반환한다")

    //6.7
    assertEqual(_ints(3)(rng2), ints(3)(rng2),
      "sequence 로 만든 _ints 는 ints 와 같은 결과를 반환한다")

    //6.8
    val (nn, _) = nonNegativeLessThan(5)(rng2)
    assertEqual(nn, 1,
      "nonNegativeLessThan(5)는 5이하의 무작위 정수를 반환한다")

    //6.9
    assertEqual(
      map(nonNegativeInt)(_ / (Int.MaxValue.toDouble + 1))(rng2),
      _map(nonNegativeInt)(_ / (Int.MaxValue.toDouble + 1))(rng2),
      "flatmap 을 이용해 만든 _map 은 map 과 같은 결과를 반환한다"
    )
    assertEqual(
      map2(_double, int)((_, _))(rng2),
      _map2(_double, int)((_, _))(rng2),
      "flatmap 을 이용해 만든 _map2 은 map2 와 같은 결과를 반환한다"
    )

    val initRNG: RNG = SimpleRNG(66578973461475L)
    (1 to 100).foldLeft(initRNG)((nowRNG, _)=>{
      val (die, newRNG) = rollDie(nowRNG)
      assert(1 <= die, s"$die 는 1보다 작습니다. $nowRNG")
      assert(die <= 6, s"$die 는 6보다 큽니다. $nowRNG")

      newRNG
    })
    println("PASS! rollDie 는 1 이상 6 이하인 값만을 반환한다.")

    val simulation = simulateMachine(List(Coin, Turn, Coin, Turn, Turn, Coin))
    val ((coins, candies), _) = simulation.run(Machine(locked = true, coins = 10, candies = 5))
    assertEqual((coins, candies), (13, 3),
      "simulateMachine 을 수행하고 나면 코인 13개 캔디 3개가 남는다.")
  }
}