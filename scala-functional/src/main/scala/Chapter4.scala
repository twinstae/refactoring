object Chapter4 {
  sealed trait Option[+A] {
    def map[B](f: A => B): Option[B] = this match {
      case None => None
      case Some(a) => Some(f(a))
    }

    def getOrElse[B >: A](default: => B): B = this match {
      case None => default
      case Some(a) => a
    }

    def flatMap[B](f: A => Option[B]): Option[B] = {
      map(f).getOrElse(None)
    }

    def orElse[B >: A](ob: => Option[B]): Option[B] =
      map((x:A) => Some(x)).getOrElse(ob)

    def filter(f: A => Boolean): Option[A] =
      if (map(f).getOrElse(false)) this
      else None
  }

  case class Some[+A](get: A) extends Option[A]
  case object None extends Option[Nothing]

  def variance(xs: Seq[Double]): Option[Double] = {
    def average(ys: Seq[Double]): Option[Double] = {
      if (ys.isEmpty) None
      else Some(ys.sum / ys.size)
    }

    average(xs).flatMap(m => average(xs.map(x => math.pow(x - m, 2))))
  }

  def main(args: Array[String]): Unit ={
    // 연습문제 4.2
    // 9 4 1 0 1 4 9 / 7 = 28 / 7 = 4.0
    println(variance(Seq(1,2,3,4,5,6,7)) == Some(4.0))
    //
  }
}