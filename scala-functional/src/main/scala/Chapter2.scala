import scala.annotation.tailrec

object Chapter2 {
  def abs(n: Int): Int =
    if (n < 0) -n
    else n

  private def formatAbs(x: Int) = {
    val msg = "The absolute value of %d is %d"
    msg.format(x, abs(x))
  }

  def factorial(n: Int): Int = {
    @tailrec
    def go(n: Int, acc: Int): Int =
      if (n <= 0) acc
      else go(n-1, n * acc)

    go(n, 1)
  }

  private def formatFactorial(x: Int) =
    "The factorial of %d is %d".format(x, factorial(x))

  def fib(n: Int): Int = {
    @tailrec
    def go(now: Int, a: Int, b: Int): Int =
      if (n == now) a
      else go(now+1, b, a+b)

    go(1, 0, 1)
  }

  private def formatFib(x: Int): String =
    "The %dth fibonacci number is %d".format(x, fib(x))

  def findFirst[T](as: Array[T], p: T => Boolean): Int = {
    @tailrec
    def loop(n: Int): Int =
      if (n >= as.length) -1
      else if (p(as(n))) n
      else loop(n+1)
    loop(0)
  }

  def isSorted[A](as: Array[A], ordered: (A,A)=> Boolean): Boolean = {
    @tailrec
    def loop(n: Int): Boolean = {
      if (n >= as.length) true
      else if (ordered(as(n-1), as(n))) loop(n+1)
      else false
    }

    loop(1)
  }

  def curry[A,B,C](f: (A,B) => C): A => (B => C) =
    (a: A) => (b: B) => f(a, b)

  def uncurry[A,B,C](f: A=>B=>C): (A,B)=>C =
    (a: A, b:B) => f(a)(b)

  def compose[A,B,C](f: B=>C, g: A=>B): A=>C =
    (a: A) => f(g(a))

  def main(args: Array[String]): Unit ={
    println(formatAbs(-42))
    println()
    println(formatFactorial(5))
    println()
    println(formatFib(3))
    println(formatFib(4))
    println(formatFib(5))
    println(formatFib(6))

    println()
    val firstIntArray = Array(1,2,3,4,5)
    println(findFirst[Int](firstIntArray, (a: Int) => a==3))
    println(isSorted[Int](firstIntArray, (a,b)=> a < b))
    val secondIntArray = Array(1,2,3,10,1)
    println(findFirst[Int](secondIntArray, (a: Int) => a==10))
    println(isSorted[Int](secondIntArray, (a,b)=> a < b))

    val curriedIsSortedInt = curry(isSorted[Int]);
    println(
      curriedIsSortedInt
      (secondIntArray)
      ((a, b) => a<b)
    ) // isSorted를 curry해서 두 번에 나눠서 parameter를 전달

    println(
      uncurry(curriedIsSortedInt)(secondIntArray, (a,b)=> a < b)
    ) // 다시 uncurry, isSorted[Int]와 같다
  }
}