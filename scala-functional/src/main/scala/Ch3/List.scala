package Ch3

import scala.annotation.tailrec

sealed trait List[+A]

case object Nil extends List[Nothing]
case class Cons[+A](head: A, tail: List[A]) extends List[A]

object List {
  @tailrec
  def sum(ints: List[Int], acc: Int = 0): Int = ints match {
    case Nil => 0
    case Cons(x, xs) => sum(xs, acc+x)
  }

  @tailrec
  def product(ds: List[Double], acc:Double =1.0): Double = ds match {
    case Nil => 1.0
    case Cons(0, _) => 0
    case Cons(x, xs) => product(xs, x * acc)
  }

  def foldRight[A, B](as: List[A], z: B)(f: (A, B) => B): B =
    as match {
      case Nil => z
      case Cons(x, xs) => f(x, foldRight(xs, z)(f))
    }

  @tailrec
  def foldLeft[A, B](as: List[A], z: B)(f: (B, A) => B): B =
    as match {
      case Nil => z
      case Cons(x, xs) => foldLeft(xs, f(z, x))(f)
    }

  def reverse[A](list: List[A]): List[A] =
    foldLeft(list, Nil: List[A])((z, x)=>Cons(x, z))

  def foldRightByLeft[A, B](l: List[A], z: B)(f: (A, B) => B): B ={
    foldLeft(reverse(l), z)((b,a) => f(a,b))
  }

  def concat[A](listOfList: List[List[A]]): List[A] =
    foldLeft(listOfList, Nil: List[A])((z, x) => append(z, x))

  def sum2(ns: List[Int]): Int =
    foldRightByLeft(ns, 0)((x, y)=>x+y)

  def product2(ns: List[Double]): Double =
    foldRightByLeft(ns, 1.0)(_ * _)

  def length[A](as: List[A]): Int = {
    foldRightByLeft(as, 0)((_, b)=>b+1)
  }

  def apply[T](as: T*): List[T] =
    if(as.isEmpty) Nil
    else Cons(as.head, apply(as.tail: _*))

  def head[A](a: List[A]): A = a match {
    case Cons(head, _) => head
    case Nil => sys.error("head of empty list")
  }

  def tail[T](list: List[T]): List[T] = list match {
    case Nil => sys.error("tail of empty list")
    case Cons(_, tail) => tail
  }

  def setHead[T](list: List[T], newHead: T): List[T] = list match {
    case Nil => sys.error("setHead on empty list")
    case Cons(_, tail) => Cons(newHead, tail)
  }

  @tailrec
  def drop[T](list: List[T], n: Int): List[T] = {
    if (n <= 0) list
    else list match {
      case Cons(head, tail) =>drop(tail, n-1)
      case Nil => Nil
    }
  }

  @tailrec
  def dropWhile[A](l: List[A], f: A => Boolean): List[A] = l match {
    case Cons(head, tail) =>
      if (f(head)) dropWhile(tail, f)
      else l
    case Nil => Nil
  }

  def init[A](l: List[A]): List[A] = {
    l match {
      case Cons(_, Nil) => Nil
      case Cons(head, tail) => Cons(head, init(tail))
      case Nil => Nil
    }
  }

  def append[A](a: List[A], b: List[A]): List[A] =
    foldRightByLeft(a, b)((xs, z)=>Cons(xs, z))

  def map[A,B](as: List[A])(f: A=>B): List[B] =
    foldRightByLeft(as, Nil: List[B])((a, listB)=>Cons(f(a), listB))

  def filter[A](as: List[A])(f: A=>Boolean): List[A] =
    foldRightByLeft(as, Nil: List[A])((a, listA)=>{
      if (f(a)) Cons(a, listA)
      else listA
    })

  def flatMap[A,B](as: List[A])(f: A=>List[B]): List[B] = concat(map(as)(f))

  def filterByFlatMap[A](as: List[A])(f: A=>Boolean): List[A] =
    flatMap(as)(a => if (f(a)) List(a) else Nil)

  def zipSum(a: List[Int], b: List[Int]): List[Int] = (a, b) match {
    case (_, Nil) => Nil
    case (Nil, _) => Nil
    case (Cons(headA, tailA), Cons(headB, tailB)) => Cons(headA+headB, zipSum(tailA, tailB))
  }

  def zipWith[A](a: List[A], b: List[A])(f:(A,A)=>A): List[A] = (a, b) match {
    case (_, Nil) => Nil
    case (Nil, _) => Nil
    case (Cons(headA, tailA), Cons(headB, tailB)) => Cons(f(headA, headB), zipWith(tailA, tailB)(f))
  }

  @tailrec
  def startsWith[A](list: List[A], prefix: List[A]): Boolean = (list, prefix) match {
    case (_, Nil) => true // 더 이상 비교할 prefix가 남지 않았다...
    case (Cons(lh,lt), Cons(hp, tp)) if lh == hp => startsWith(lt, tp) // 같으면 다음 값을 비교
    case _ => false // prefix의 head와 같지 않다
  }

  @tailrec
  def hasSubsequence[A](sup: List[A], sub: List[A]): Boolean = sup match {
    case Nil => sub == Nil
    case _ if startsWith(sup, sub) => true
    case Cons(_, t) => hasSubsequence(t, sub)
  }
}

object test_list {
  def main(args: Array[String]): Unit ={
    // 패턴 부합
    val x = List(1,2,3,4,5) match {
      case Cons(x, Cons(2, Cons(4, _))) => x
      case Nil => 42
      case Cons(x, Cons(y,  Cons(3,  Cons(4, _)))) => x + y // here!
      case Cons(h, t) => h + List.sum(t)
      case _ => 101
    }
    println(x == 3)

    println(List.tail(List(1,2,3,4,5))
      == List(2,3,4,5))
    println(List.setHead(List(1,2,3,4,5), 8)
      == List(8,2,3,4,5))
    println(List.drop(List(1,2,3,4,5), 3)
      == List(4,5))
    println(List.dropWhile(List(1,2,3,4,5), (a: Int) => a < 3)
      == List(3,4,5))
    println(List.init(List(1,2,3,4))
      == List(1,2,3))

    println(List.sum2(List(1,2,3,4))
      == 10)
    println(List.product2(List(1.0, 2.0, 3.0, 4.0))
      == 24.0)
    // 3.8
    println(List.foldRight(List(1, 2, 3), Nil: List[Int])((a, b)=>Cons(a * 2,b))
      == List(2,4,6))
    // 3.9
    println(List.length(List(2,2,2))
      == 3)
    // 3.10, 3.11
    println(List.foldLeft(List(1, 2, 3), 0: Int)(_+_)
      == 6)
    println(List.foldLeft(List(1.0, 2.0, 3.0, 4.0), 1.0: Double)(_*_)
      == 24.0)
    // 3.12
    println(List.reverse(List(1,2,3,4))
      ==List(4,3,2,1))
    // 3.13 == foldRigthByLeft
    // 3.14
    println(List.append(List(1,2,3), List(1,2,3))
      ==List(1,2,3,1,2,3))
    // 3.15
    println(List.concat(List(List(1,2,3), List(1,2,3)))
      ==List(1,2,3,1,2,3))
    // 3.16
    println(List.foldRightByLeft(List(1,2,3), Nil: List[Int])((x, z)=>Cons(x+1, z))
      == List(2,3,4))
    // 3.17
    println(List.foldRightByLeft(List(1.0,2.0,3.0), Nil: List[String])((x, z)=>Cons(x.toString, z))
      == List("1.0", "2.0", "3.0"))
    // 3.18
    println(List.map(List(1,2,3))((a)=>a*a)
      == List(1,4,9))
    // 3.19
    println(List.filter(List(1,2,3,4,5,6))(_ % 2 == 0)
      == List(2,4,6))
    // 3.20
    println(List.flatMap(List(1,2,3))(i=> List(i,i))
      == List(1,1,2,2,3,3))
    // 3.21
    println(List.filterByFlatMap(List(1,2,3,4,5,6))(_ % 2 == 0)
      == List(2,4,6))
    // 3.22
    println(List.zipSum(List(1,2,3), List(4,5,6))
      == List(5,7,9))
    // 3.23
    println(List.zipWith(List(1,2,3), List(4,5,6))(_*_)
      == List(4,10,18))
    // 3.24
    println(List.hasSubsequence(List(1, 2, 3, 4, 5, 6), List(4, 5)))
  }
}
