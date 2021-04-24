package Ch6
import Reducer._

case class Reducer[S, +A](run: S => (A, S)) {
  def map[B](f: A => B): Reducer[S, B] =
    flatMap(a => unit(f(a)))
  def map2[B,C](sb: Reducer[S, B])(f: (A, B) => C): Reducer[S, C] =
    flatMap(a => sb.map(b => f(a, b)))
  def flatMap[B](f: A => Reducer[S, B]): Reducer[S, B] = Reducer(s => {
    val (a, s1) = run(s)
    f(a).run(s1)
  })
}

object Reducer {
  type Rand[A] = Reducer[RNG, A]

  def unit[S, A](a: A): Reducer[S, A] =
    Reducer(s => (a, s))

  def sequence[S, A](l: List[Reducer[S, A]]): Reducer[S, List[A]] = {
    l.reverse.foldLeft(unit[S, List[A]](List())) ((acc, f) => f.map2(acc)( _ :: _ ))
  }

  def modify[S](f: S => S): Reducer[S, Unit] = for {
    s <- get
    _ <- set(f(s))
  } yield ()

  def get[S]: Reducer[S, S] = Reducer(s => (s, s))

  def set[S](s: S): Reducer[S, Unit] = Reducer(_ => ((), s))
}

sealed trait Input
case object Coin extends Input
case object Turn extends Input

case class Machine(locked: Boolean, candies: Int, coins: Int)

object Candy {
  def update: Input => Machine => Machine =
    (input: Input) => (machine: Machine) =>
      (input, machine) match {
        case (_, Machine(_, 0, _)) => machine // 캔디가 없으면 무시
        case (Coin, Machine(false, _, _)) => machine // 열린 판매기에 동전을 넣으면 무시
        case (Turn, Machine(true, _, _)) => machine // 잠긴 판매기 손잡이를 돌리면 무시
        case (Coin, Machine(true, candies, coins)) =>
          Machine(locked = false, candies, coins + 1) // 동전을 넣으면 열린다
        case (Turn, Machine(false, candies, coins)) =>
          Machine(locked = true, candies - 1, coins) // 손잡이를 돌리면 사탕, 잠긴다
      }

  def simulateMachine(inputs: List[Input]): Reducer[Machine, (Int, Int)] = for {
    _ <- sequence(inputs.map(input=>
        modify[Machine](update(input))))
    s <- get
  } yield (s.coins, s.candies)
}