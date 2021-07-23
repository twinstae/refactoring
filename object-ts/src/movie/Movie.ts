import Money from './Money';
import DiscountPolicy from './DiscountPolicy';

export default class Movie {
  _title: string;
  _fee: Money;
  _discountPolicy: DiscountPolicy;

  constructor(title: string, fee: Money, discountPolicy: DiscountPolicy) {
    this._title = title;
    this._fee = fee;
    this._discountPolicy = discountPolicy;
  }

  getFee(): Money {
    return this._fee;
  }

  calculateMovieFee({ startTime, isSequence }): Money {
    const discountAmount = this._discountPolicy.calculateDiscountAmount({
      startTime,
      isSequence,
      fee: this._fee,
    });
    return this._fee.minus(discountAmount);
  }
}
