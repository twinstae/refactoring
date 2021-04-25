package fpinscala.testing
import fpinscala.laziness.Stream
import fpinscala.state.RNG
import fpinscala.state.Reducer
import fpinscala.parallelism._
import fpinscala.parallelism.Par.Par

case class Gen[A](sample: Reducer[RNG, A]) {
  def flatMap[B](f: A => Gen[B]): Gen[B] =
    Gen(sample.flatMap(a => f(a).sample))

  def listOfN(size: Int): Gen[List[A]] =
    Gen.listOfN(size, this)
}

object Gen {
  // 연습문제 8.4
  def choose(start: Int, stopExclusive: Int): Gen[Int] =
    Gen(Reducer(RNG.nonNegativeInt).map(n => start + n % (stopExclusive - start)))

  // 놀이
  def chooseInts(size: Int)(start: Int, stopExclusive: Int): Gen[List[Int]] = 
    Gen.listOfN(size, Gen.choose(start, stopExclusive))

  // 연습문제 8.5
  def unit[A](a: => A): Gen[A] =
    Gen(Reducer.unit(a))

  val boolean: Gen[Boolean] =
    Gen(Reducer(RNG.boolean))

  def listOfN[A](n: Int, g: Gen[A]): Gen[List[A]] =
    Gen(Reducer.sequence(List.fill(n)(g.sample)))
}
