package fpinscala.laziness

import fpinscala.laziness.Stream.{cons, empty}

import scala.annotation.tailrec

sealed trait Stream[+A]{
  def toList: List[A] = this match {
    case Cons(h, t) => h() :: t().toList
    case _ => List()
  }

  def take(n: Int): Stream[A] = {
    this match {
      case Cons(h, t) if n > 0 => cons[A](h(), t().take(n - 1))
      case _ => empty
    }
  }

  @tailrec
  final def drop(n: Int): Stream[A] = {
    this match {
      case Cons(_, t) if n > 0 => t().drop(n - 1)
      case _ => this
    }
  }

  def takeWhile(p: A => Boolean): Stream[A] =
    foldRight[Stream[A]](empty)((head, tail)=>{
      if (p(head)) cons[A](head, tail)
      else empty
    })

  def headOption: Option[A] =
    foldRight(None: Option[A])((head, _) => {if (head != Empty) Some(head) else None})

  def foldRight[B](z: => B)(f: (A, =>B) => B): B =
    this match {
      case Cons(h,t) => f(h(), t().foldRight(z)(f))
      case _ => z
    }

  def anyExist(p: A => Boolean): Boolean =
    foldRight(false)((a,b) => p(a) || b)

  def forAll(p: A => Boolean): Boolean =
    foldRight(true)((a, b) => p(a) && b)
}
case object Empty extends Stream[Nothing]
case class Cons[+A](h: () => A, t: () => Stream[A]) extends Stream[A]

object Stream {
  def cons[A](hd: => A, tl: => Stream[A]): Stream[A] = {
    lazy val head = hd
    lazy val tail = tl
    Cons(() => head, () => tail)
  }
  def empty[A]: Stream[A] = Empty
  def apply[A](as: A*): Stream[A] =
    if (as.isEmpty) empty else cons(as.head, apply(as.tail: _*))

  def expect[T](result: T, expect: T): Unit ={
    print(result)
    print(" ")
    println(if (result.equals(expect)) "PASS!" else expect)
  }

  def main(args: Array[String]): Unit ={
    val s = Stream(1, 2, 3, 4)
    println("5.1 toList")
    expect(s.toList, List(1,2,3,4))

    println("\n5.2 take, drop")
    expect(s.take(2).toList, List(1,2))
    expect(s.drop(0).toList, List(1,2,3,4))
    expect(s.drop(2).toList, List(3,4))

    println("\n5.3 5.5 takeWhile")
    expect(s.takeWhile((it: Int) => {it <= 3}).toList, List(1,2,3))

    println("\n5.4.1 anyExist")
    expect(s.anyExist((it: Int) => {it == 3}), true)
    expect(s.anyExist((it: Int) => {it == 5}), false)

    println("\n5.4.2 forAll")
    expect(s.forAll((it: Int) => {it < 5}), true)
    expect(s.forAll((it: Int) => {it < 3}), false)

    println("\n5.6 headOption")
    expect(s.headOption, Some(1))
    expect(Empty.headOption, None)
  }
}
