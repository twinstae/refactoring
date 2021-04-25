package fpinscala.testing

import Prop._
import fpinscala.testing.Gen
import fpinscala.testing.Gen._
import fpinscala.testing.SGen
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
    s"test case: $s \n\n" +
    s"generated an exception: ${e.getMessage()}" +
    "stack trace:\n" + e.getStackTrace.slice(0, 20).mkString("\n")

  def run(
    p: Prop,
    maxSize: Int = 100, // A default argument of `200`
    testCases: Int = 100,
    rng: RNG = RNG.SimpleRNG(System.currentTimeMillis)
  ): Unit = {
      p.run(maxSize, testCases, rng) match {
        case Falsified(msg, n) => println(s"Falsified! test failed after $n test:\n $msg \n")
        case Passed => println(s"Ok! Passed $testCases tests\n")
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

    길이가_1_이상인_리스트("에서 최댓값을 찾으면 더 큰 값이 존재하지 않는다."){
      l =>
        val max = l.max
        !l.exists(_ > max)
    }

    길이가_1_이상인_리스트("를 정렬했을 때 처음과 끝은 각각 최솟값, 최댓값이다."){
      l =>
        val sortedList = l.sorted
      
        sortedList.max == sortedList.last &&
        sortedList.min == sortedList(0)
    }
 
    길이가_1_이상인_리스트("를 정렬했을 때 리스트의 크기는 변하지 않는다."){
      l =>
        val initSize = l.size
        val sortedList = l.sorted
      
        sortedList.size == initSize
    }
  }

  def 길이가_1_이상인_리스트(msg: String,
      g: Gen[Int] = Gen.choose(-10, 10)
    )(expect: List[Int] =>Boolean){
    val sortedProp = forAll(Gen.listOf1(g)) { 
      l => expect(l)
    }
    println("길이가 1 이상인 리스트" + msg)
    Prop.run(sortedProp)
  }
}
