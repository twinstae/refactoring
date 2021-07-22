import Money from "../movie/Money";
import DiscountCondtion, {get_is_discountable} from "./DiscountCondition";
import Screening from "./Screening";

export enum MovieType {
  AMOUNT_DISCOUNT,
  PERCENT_DISCOUNT,
  NONE_DISCOUNT,
}

export default class Movie {
  title: string
  fee: Money
  discountCondtions: DiscountCondtion[]

  movieType: MovieType
  discountAmount: Money
  discountPercent: number

  constructor(
    title: string,
    fee: Money,
    discountCondtion: DiscountCondtion[]
  ){
    this.title = title;
    this.fee = fee;
    this.discountCondtions = discountCondtion;
  }
}


export function calculateDiscountAmount(screening: Screening){
  if (! get_is_discountable(screening)){
    return Money.ZERO;
  }

  const movie = screening.movie;

  if (movie.movieType == MovieType.AMOUNT_DISCOUNT){
    return movie.discountAmount;
  } else if (movie.movieType == MovieType.PERCENT_DISCOUNT){
    return movie.fee.times(movie.discountPercent);
  } else {
    return Money.ZERO;
  }
}
