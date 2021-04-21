package Ch6
import State._

case class State[S, +A](run: S => (A, S)) {
  def map[B](f: A => B): State[S, B] =
    flatMap(a => unit(f(a)))
  def map2[B,C](sb: State[S, B])(f: (A, B) => C): State[S, C] =
    flatMap(a => sb.map(b => f(a, b)))
  def flatMap[B](f: A => State[S, B]): State[S, B] = State(s => {
    val (a, s1) = run(s)
    f(a).run(s1)
  })
}

object State {
  type Rand[A] = State[RNG, A]

  def unit[S, A](a: A): State[S, A] =
    State(s => (a, s))

  def sequence[S, A](l: List[State[S, A]]): State[S, List[A]] = {
    l.reverse.foldLeft(unit[S, List[A]](List())) ((acc, f) => f.map2(acc)( _ :: _ ))
  }

  def modify[S](f: S => S): State[S, Unit] = for {
    s <- get
    _ <- set(f(s))
  } yield ()

  def get[S]: State[S, S] = State(s => (s, s))

  def set[S](s: S): State[S, Unit] = State(_ => ((), s))
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

  def simulateMachine(inputs: List[Input]): State[Machine, (Int, Int)] = for {
    _ <- sequence(inputs.map(input=>
        modify[Machine](update(input))))
    s <- get
  } yield (s.coins, s.candies)
}