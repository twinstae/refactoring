import Money from '../movie/Money';
import { DiscountCondtion, satisfiedCondition } from './DiscountCondition';

export type Movie = {
  title: string;
  fee: Money;
  discountCondtions: DiscountCondtion[];
  calculateDiscount: DiscountFunc;
};

interface ScreeningDto {
  startTime: Date;
  sequence: number;
}

export function get_is_discountable(screeningDto: ScreeningDto, movie: Movie) {
  return movie.discountCondtions.some((cond) => satisfiedCondition(screeningDto, cond));
}

export type DiscountFunc = (fee: Money) => Money;
export function createAmountDiscount(amount: Money): DiscountFunc {
  return (_) => amount;
}

export function createPercentDiscount(percent: number): DiscountFunc {
  return (fee: Money) => fee.times(percent);
}

export function calculateMovieFee(movie: Movie, screeningDto: ScreeningDto) {
  if (!get_is_discountable(screeningDto, movie)) {
    return movie.fee;
  }
  const discountAmount = movie.calculateDiscount(movie.fee);
  return movie.fee.minus(discountAmount);
}
