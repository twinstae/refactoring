import Money from "../movie/Money";
import DiscountCondtion from "./DiscountCondition";
import { satisfiedCondition } from "./DiscountCondition";

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

interface ScreeningDto {
  startTime: Date,
  sequence: number
}

export function get_is_discountable(
  screeningDto: ScreeningDto,
  movie: Movie
){
  return movie.discountCondtions.some((cond)=> satisfiedCondition(screeningDto, cond));
}

export function calculateDiscountAmount(movie: Movie){
  if (movie.movieType == MovieType.AMOUNT_DISCOUNT){
    return movie.discountAmount;
  } else if (movie.movieType == MovieType.PERCENT_DISCOUNT){
    return movie.fee.times(movie.discountPercent);
  } else {
    return Money.ZERO;
  }
}

export function calculateMovieFee(movie: Movie, screeningDto: ScreeningDto){
  if (! get_is_discountable(screeningDto, movie)){
    return movie.fee;
  }
  const discountAmount = calculateDiscountAmount(movie);
  return movie.fee.minus(discountAmount);
}
