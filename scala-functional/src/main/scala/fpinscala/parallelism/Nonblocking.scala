package fpinscala.parallelism

import java.util.concurrent.{Callable, CountDownLatch, ExecutorService, Executors}
import java.util.concurrent.atomic.AtomicReference
import fpinscala.parallelism.Actor._
import fpinscala.parallelism.Nonblocking.Par.{unit, unit_list}

import language.implicitConversions

object Nonblocking {
  trait Future[+A] {
    private[parallelism] def apply(k: A => Unit): Unit
  }

  type Par[+A] = ExecutorService => Future[A]

  object Par {
    def run[A](es: ExecutorService)(p: Par[A]): A = {
      val ref = new AtomicReference[A]
      val latch = new CountDownLatch(1)
      p(es) { a => ref.set(a); latch.countDown() }
      latch.await()
      ref.get()
    }

    def unit[A](a: A): Par[A] =
      es => (k: A => Unit) => k(a)

    def unit_list[A](a_list: List[A]): List[Par[A]] =
      a_list.map(unit)

    def fork[A](a: => Par[A]): Par[A] =
      es => (cb: A => Unit) => eval(es)(a(es)(cb))

    def eval(es: ExecutorService)(r: => Unit): Unit =
      es.submit(new Callable[Unit] { def call: Unit = r })

    def map2[A, B, C](p: Par[A], p2: Par[B])(f: (A, B) => C): Par[C] =
      es => (cb: C => Unit) => {
        var ar: Option[A] = None
        var br: Option[B] = None

        val combiner = Actor[Either[A, B]](es) {
          case Left(a) => br match {
            case None => ar = Some(a)
            case Some(b) => eval(es)(cb(f(a, b)))
          }
          case Right(b) => ar match {
            case None => br = Some(b)
            case Some(a) => eval(es)(cb(f(a, b)))
          }
        }

        p(es)(a => combiner ! Left(a))
        p2(es)(b => combiner ! Right(b))
      }

    def map[A,B](p: Par[A])(f: A => B): Par[B] =
      es =>
        (cb: B => Unit) =>
          p(es)(a => eval(es) {
            cb(f(a))
          })

    def lazyUnit[A](a: => A): Par[A] =
      fork(unit(a))

    def asyncF[A,B](f: A => B): A => Par[B] =
      a => lazyUnit(f(a))

    def sequenceRight[A](as: List[Par[A]]): Par[List[A]] =
      as match {
        case Nil => unit(Nil)
        case h :: t => map2(h, fork(sequence(t)))(_ :: _)
      }

    def sequenceBalanced[A](as: IndexedSeq[Par[A]]): Par[IndexedSeq[A]] = fork {
      if (as.isEmpty) unit(Vector())
      else if (as.length == 1) map(as.head)(a => Vector(a))
      else {
        val (l,r) = as.splitAt(as.length/2)
        map2(sequenceBalanced(l), sequenceBalanced(r))(_ ++ _)
      }
    }

    def sequence[A](as: List[Par[A]]): Par[List[A]] =
      map(sequenceBalanced(as.toIndexedSeq))(_.toList)

    def parMap[A,B](as: List[A])(f: A => B): Par[List[B]] =
      sequence(as.map(asyncF(f)))

    def parMap[A,B](as: IndexedSeq[A])(f: A => B): Par[IndexedSeq[B]] =
      sequenceBalanced(as.map(asyncF(f)))

    def choiceN[A](pn: Par[Int])(choices: List[Par[A]]): Par[A] =
      chooser(pn)(choices(_))

    def choice[A](cond: Par[Boolean])(t: Par[A], f: Par[A]): Par[A] =
      chooser(cond)(if(_) t else f)

    def chooser[A, B](pa: Par[A])(choices: A => Par[B]): Par[B] =
      flatMap(pa)(choices)

    def flatMap[A, B](a: Par[A])(f: A => Par[B]): Par[B] =
      join(map(a)(f))

    def join[A](a: Par[Par[A]]): Par[A] =
      es => run(es)(a)(es)

  }

  def assertEqual[T](actual: T, expected: T, passMsg: String=""): Unit = {
    val message = s"\n expected: $expected\n actual  : $actual"
    assert(expected == actual, message)
    println("PASS! "+passMsg)
  }

  def assertParEqual[T](es: ExecutorService)(p: Par[T], p2: Par[T], passMsg: String=""): Unit = {
    val expected = Par.run(es)(p)
    val actual = Par.run(es)(p2)
    val message = s"\n expected: $expected\n actual  : $actual"
    assert(expected == actual, message)
    println("PASS! "+passMsg)
  }

  def main(args: Array[String]): Unit = {
    val p = Par.parMap(List.range(1, 100000))(math.sqrt(_))

    val es = Executors.newFixedThreadPool(4)
    val x: List[Double] = Par.run(es)(p)

    assertEqual(x.slice(0, 10), List(
      1.0,
      1.4142135623730951,
      1.7320508075688772,
      2.0,
      2.23606797749979,
      2.449489742783178,
      2.6457513110645907,
      2.8284271247461903,
      3.0,
      3.1622776601683795
    ))

    assertParEqual(es)(Par.choiceN(unit(1))(unit_list(List("영", "일"))), unit("일"))
    assertParEqual(es)(Par.choice(unit(true))(unit("참"), unit("거짓")), unit("참"))
    val map = Map(1->"일", 2->"이", 3->"삼")
    assertParEqual(es)(Par.chooser(unit(3))(n => unit(map.getOrElse(n, "없음"))), unit("삼"))
    es.shutdown()
    println("shutdown")
  }
}
