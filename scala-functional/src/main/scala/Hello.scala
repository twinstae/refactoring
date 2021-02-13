import scala.annotation.tailrec

object Hello {
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
    def go(now: Int, a: Int, b: Int): Int =
      if (n == now) a
      else go(now+1, b, a+b)

    go(1, 0, 1)
  }

  private def formatFib(x: Int): String =
    "The %dth fibonacci number is %d".format(x, fib(x))

  def main(args: Array[String]): Unit ={
    println(formatAbs(-42))
    println()
    println(formatFactorial(5))
    println()
    println(formatFib(3))
    println(formatFib(4))
    println(formatFib(5))
    println(formatFib(6))
  }
}