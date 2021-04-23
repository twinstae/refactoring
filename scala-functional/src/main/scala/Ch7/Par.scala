package Ch7

import java.util.concurrent.{Callable, ExecutorService, Executors, Future, TimeUnit}

import scala.::

object Par {
  type Par[A] = ExecutorService => Future[A]

  def run[A](es: ExecutorService)(a: Par[A]): Future[A] = a(es)

  def unit[A](a: A): Par[A] = (es: ExecutorService) => UnitFuture(a)
  def lazyUnit[A](a: =>A): Par[A] = delay(unit(a))

  def asyncF[A,B](f: A => B): A => Par[B] =
    a => lazyUnit(f(a))

  private case class UnitFuture[A](get: A) extends Future[A] {
    def isDone = true
    def get(timeout: Long, units: TimeUnit): A = get
    def isCancelled = false
    def cancel(evenIfRunning: Boolean): Boolean = false
  }

  def sumByFold(ints: Seq[Int]): Int = {
    ints.foldLeft(0)((b, a)=> b + a)
  }

  def sumByDC(ints: Seq[Int]): Int = {
    if (ints.size <= 1)
      ints.headOption getOrElse 0
    else {
      val (l, r) = ints.splitAt(ints.length / 2)
      sumByDC(l) + sumByDC(r)
    }
  }

  def map2[A,B,C](a: Par[A], b:Par[B])(f: (A,B) => C): Par[C] =
    (es: ExecutorService) => {
      val af = a(es)
      val bf = b(es)
      UnitFuture(f(af.get, bf.get))
    }

  def map[A, B](pa: Par[A])(f: A=>B): Par[B] =
    map2(pa, unit(()))((a, _)=> f(a))

  def sortPar(parList: Par[List[Int]]): Par[List[Int]] = map(parList)(_.sorted)

  def sequence[A](fbs: List[Par[A]]): Par[List[A]] = {
    fbs.foldRight[Par[List[A]]](unit(List()))((h, t) => map2(h, t)(_ :: _))
  }

  def parMap[A, B](ps: List[A])(f: A => B): Par[List[B]] = delay {
    sequence(ps.map(asyncF(f)))
  }

  def parFilter[A](as: List[A])(f: A => Boolean): Par[List[A]] = {
    val pars: List[Par[List[A]]] =
      as map asyncF((a: A) => if (f(a)) List(a) else List())
    map(sequence(pars))(_.flatten)
  }


  def delay[A](a: => Par[A]): Par[A] = {
    es => a(es)
  }

  def sum(ints: Seq[Int]): Par[Int] = {
    if (ints.size <= 1)
      Par.unit(ints.headOption getOrElse 0)
    else {
      val (l, r) = ints.splitAt(ints.length / 2)
      Par.map2(Par.delay(sum(l)), Par.delay(sum(r)))(_ + _)
    }
  }

  def assertEqual[T](actual: T, expected: T, passMsg: String=""): Unit = {
    val message = s"\n expected: $expected\n actual  : $actual"
    assert(expected == actual, message)
    println("PASS! "+passMsg)
  }

  def equal[A](es: ExecutorService)(p: Par[A], p2: Par[A]): Boolean =
    p(es).get == p2(es).get

  def assertParEqual[T](es: ExecutorService)(p: Par[T], p2: Par[T], passMsg: String=""): Unit = {
    val expected = p(es).get
    val actual = p2(es).get
    val message = s"\n expected: $expected\n actual  : $actual"
    assert(expected == actual, message)
    println("PASS! "+passMsg)
  }

  def main(args: Array[String]): Unit = {
    val expected = 512 - 1
    val ints = List(1, 2, 4, 8, 16, 32, 64, 128, 256)
    assertEqual(sumByFold(ints), expected)
    assertEqual(sumByDC(ints), expected)
    val es = Executors.newFixedThreadPool(4)
    assertParEqual(es)(sum(ints), unit(expected), "비동기도 결과는 같다")
  }
}