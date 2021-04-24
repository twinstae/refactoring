package testing

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
}

object Prop {
  type TestCases = Int
  type MaxSize = Int
  type FailedCase = String
  type SuccessCount = Int
  type Result = Either[FailedCase, (Status, TestCases)]

  def check(p: => Boolean): Prop =
    forAll(unit(()))(_ => p)

  def run

  def forAll[A](a: Gen[A])(f: A => Boolean): Prop
}
