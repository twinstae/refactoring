package fpinscala.testing

import Prop._
import fpinscala.state.Reducer
import fpinscala.state.RNG

case class Prop(run: (MaxSize, TestCases, RNG) => Result) {
  def &&(p: Prop) = Prop {
    (max, n, rng) => run(max, n, rng) match {
      case Falsified(failure, successes) => Falsified(failure, successes)
      case Passed => p.run(max, n, rng) match {
        case Falsified(failure, successes) => Falsified(failure, n + successes)
        case Passed => Passed
      }
    }
  }

  def ||(p: Prop) = Prop {
    (max, n, rng) => run(max, n, rng) match {
      case Falsified(failure, successes) =>
        p.run(max, n, rng) match {
          case Falsified(failure2, successes) =>
            Falsified(failure + "\n" + failure2, n + successes)
          case Passed => Passed
        }
      case Passed => Passed
    }
  }

}

object Prop {
  type MaxSize = Int
  type TestCases = Int
  type SuccessCount = Int
  type FailedCase = String

  sealed trait Result {
    def isFalsified: Boolean
  }

  case object Passed extends Result {
    def isFalsified: Boolean = false
  }

  case class Falsified(
    failure: FailedCase,
    successes: SuccessCount
  ) extends Result {
    def isFalsified: Boolean = true
  }

  def forAll[A](a: Gen[A])(f: A => Boolean): Prop = Prop {
    (max, n, rng) => {
      randomStream(a)(rng).zip(Stream.from(0)).take(n).map {
      case (a, i) => try {
        if (f(a)) Passed else Falsified(a.toString, i) 
      } catch {
        case e: Exception => Falsified(buildMsg(a, e), i)
      }
    }.find(_.isFalsified).getOrElse(Passed)
    }
  }

  case class Sized[A](forSize: Int => Gen[A]) extends SGen[A]
  case class Unsized[A](get: Gen[A]) extends SGen[A]

  implicit def unsized[A](g: Gen[A]): SGen[A] = Unsized(g)

  def forAll[A](sg: SGen[A])(f: A => Boolean): Prop = sg match {
    case Unsized(g2) => forAll(g2)(f)
    case Sized(gs) => forAll(gs)(f)
  }

  def forAll[A](g: Int => Gen[A])(f: A => Boolean): Prop = Prop {
    (max, n, rng) => {
      val casesPerSize = n / max + 1
      val props: Stream[Prop] = 
        Stream.from(0).take((n min max) + 1).map(i => forAll(g(i))(f))
      val prop: Prop =
        props.map(p => Prop { (max, _, rng) =>
          p.run(max, casesPerSize, rng)
        }).toList.reduce(_ && _)

      prop.run(max, n, rng)
    }
  }

  def randomStream[A](g: Gen[A])(rng: RNG): Stream[A] =
    Stream.unfold(rng)(rng => Some(g.sample.run(rng)))

  def buildMsg[A](s: A, e: Exception): String =
    s"test case: $s\n" +
    s"generated an exception: ${e.getMessage()}" +
     "stack trace:\n " + e.getStackTrace.mkString("\n")

  def run(
    p: Prop,
    maxSize: Int = 100, // A default argument of `200`
    testCases: Int = 100,
    rng: RNG = RNG.SimpleRNG(System.currentTimeMillis)
  ): Unit = {
      p.run(maxSize, testCases, rng) match {
        case Falsified(msg, n) => println(s"! test failed after $n test:\n $msg")
        case Passed => println(s"Ok! Passed $testCases tests")
      }
  }
}



sealed trait Status {}

object Status {
  case object Exhausted extends Status
  case object Proven extends Status
  case object Unfalsified extends Status
}

object test_pbt {
  def main(args: Array[String]): Unit = {
    val smallInt = Gen.choose(-10, 10)
    val maxProp = forAll(Gen.listOf(smallInt)) { intList =>
      val max = intList.max

      !intList.exists(_ > max)
    }

    Prop.run(maxProp)
  }
}

case class Gen[A](sample: Reducer[RNG, A]) {
  def listOfN(size: Int): Gen[List[A]] =
    Gen.listOfN(size, this)

  // 연습문제 8.6
  def flatMap[B](f: A => Gen[B]): Gen[B] =
    Gen(sample.flatMap(a => f(a).sample))

  def listOfN(size: Gen[Int]): Gen[List[A]] = 
    size flatMap (n => this.listOfN(n))

  def unsized: SGen[A] =
    Unsized(this)
}

object Gen {
  // 연습문제 8.4
  def choose(start: Int, stopExclusive: Int): Gen[Int] =
    Gen(Reducer(RNG.nonNegativeInt).map(n => start + n % (stopExclusive - start)))

  val double: Gen[Double] = 
    Gen(Reducer(RNG.double))

  // 놀이
  def chooseList(size: Int)(start: Int, stopExclusive: Int): Gen[List[Int]] = 
    Gen.listOfN(size, Gen.choose(start, stopExclusive))

  // 연습문제 8.5
  def unit[A](a: => A): Gen[A] =
    Gen(Reducer.unit(a))

  val boolean: Gen[Boolean] =
    Gen(Reducer(RNG.boolean))

  def listOfN[A](n: Int, g: Gen[A]): Gen[List[A]] =
    Gen(Reducer.sequence(List.fill(n)(g.sample)))

  // 연습문제 8.7
  def union[A](g1: Gen[A], g2: Gen[A]): Gen[A] =
    Gen.boolean flatMap (if (_) g1 else g2)

  // 연습문제 8.8
  def weighted[A](g1: (Gen[A], Double), g2: (Gen[A], Double)): Gen[A] = {
    val threshold = g1._2.abs / (g1._2.abs + g2._2.abs)

    Gen.double flatMap (d => if(d < threshold) g1._1 else g2._1)
  }

  def listOf[A](g: Gen[A]): SGen[List[A]] =
    Sized(size=>listOfN(size, g))
}

trait SGen[+A]
