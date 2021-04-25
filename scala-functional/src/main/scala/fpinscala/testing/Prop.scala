package testing

import fpinscala.state.RNG
import Prop._
import fpinscala.testing.Gen

case class Prop(run: (TestCases, RNG) => Result) {
  def &&(p: Prop) = Prop {
    (n, rng) => run(n, rng) match {
      case Falsified(failure, successes) => Falsified(failure, successes)
      case Passed => p.run(n, rng) match {
        case Falsified(failure, successes) => Falsified(failure, n + successes)
        case Passed => Passed
      }
    }
  }

  def ||(p: Prop) = Prop {
    (n, rng) => run(n, rng) match {
      case Falsified(failure, successes) =>
        p.run(n, rng) match {
          case Falsified(failure2, successes) =>
            Falsified(failure + "\n" + failure2, n + successes)
          case Passed => Passed
        }
      case Passed => Passed
    }
  }

}

object Prop {
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
    (n, rng) => randomStream(a)(rng).zip(Stream.from(0)).take(n).map {
      case (a, i) => try {
        if (f(a)) Passed else Falsified(a.toString, i) 
      } catch {
        case e: Exception => Falsified(buildMsg(a, e), i)
      }
    }.find(_.isFalsified).getOrElse(Passed)
  }

  def randomStream[A](g: Gen[A])(rng: RNG): Stream[A] =
    Stream.unfold(rng)(rng => Some(g.sample.run(rng)))

  def buildMsg[A](s: A, e: Exception): String =
    s"test case: $s\n" +
    s"generated an exception: ${e.getMessage()}" +
     "stack trace:\n " + e.getStackTrace.mkString("\n")
}



sealed trait Status {}

object Status {
  case object Exhausted extends Status
  case object Proven extends Status
  case object Unfalsified extends Status
}
