package testing

import fpinscala.state.RNG
import Prop._

case class Prop(run: (MaxSize, TestCases, RNG) => Result) {
  def &&(p: Prop) = Prop {
    (max, n, rng) => run(max, n, rng) match {
      case Right((a,n)) => p.run(max, n, rng).right.map { case (s,m) => (s, n+m)}
      case l => l
    }
  }
  def ||(p: Prop) = Prop {
    (max, n, rng) => run(max, n, rng) match {
      case Left(msg) => p.tag(msg).run(max, n, rng)
      case l => l
    }
  }

  def tag(msg: String) = Prop {
    (max,n,rng) => run(max,n,rng) match {
      case Left(e) => Left(msg + "\n" + e)
      case r => r
    }
  }
}

object Prop {
  type TestCases = Int
  type MaxSize = Int
  type FailedCase = String
  type SuccessCount = Int
  type Result = Either[FailedCase, (Status, TestCases)]
}

sealed trait Status {}

object Status {
  case object Exhausted extends Status
  case object Proven extends Status
  case object Unfalsified extends Status
}
