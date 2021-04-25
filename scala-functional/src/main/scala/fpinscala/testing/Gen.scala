package fpinscala.testing
import fpinscala.laziness.Stream
import fpinscala.state.RNG
import fpinscala.state.Reducer
import fpinscala.parallelism._
import fpinscala.parallelism.Par.Par

case class Gen[A](sample: Reducer[RNG, A])
