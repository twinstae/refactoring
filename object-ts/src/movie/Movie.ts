import Screening from "./Screening";
import Money from "./Money";

export default class Movie {
  _title: string
  _runningTime: Duration;
  _fee: Money;
  _discountPolicy: DiscountPolicy;

  constructor(
    title: string,
    runningTime: Duration,
    fee: Money,
    discountPolicy: DiscountPolicy,
  ){
    this._title = title;
    this._runningTime = runningTime;
    this._fee = fee;
    this._discountPolicy = discountPolicy;
  }

  getFee(): Money {
    return this._fee;
  }

  calculateMovieFee(screening: Screening): Money {
    const discountAmount = this._discountPolicy.calculateDiscountAmount(screening);
    return this._fee.minus(discountAmount);
  }
}
