package testing

case class Gen[A](sample: State[RNG, A])

