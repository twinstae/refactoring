import Money from "./Money";
import Screening from "./Screening";
import DiscountCondition, {NeverDiscountCondition} from "./DiscountCondition";

export default abstract class DiscountPolicy {
  _conditions = [];

  constructor(conditions: DiscountCondition[]){
    this._conditions = conditions;
  }

  calculateDiscountAmount(screening: Screening): Money{
    for (const each of this._conditions){
      if (each.isSatisfiedBy(screening)){
        return this._getDiscountAmount(screening)
      }
    }

    return Money.ZERO;
  }

  abstract _getDiscountAmount(screening: Screening): Money;
}


export class AmountDiscountPolicy extends DiscountPolicy {
  _discountAmount: Money

  constructor(discountAmount: Money, conditions: DiscountCondition[]){
    super(conditions);
    this._discountAmount = discountAmount;
  }

  _getDiscountAmount(): Money {
    return this._discountAmount;
  }
}

export const NoneDiscountPolicy = new AmountDiscountPolicy(Money.ZERO, [NeverDiscountCondition]);

export class PercentDiscountPolicy extends DiscountPolicy {
  _percent: number;

  constructor(percent: number, conditions: DiscountCondition[]){
    super(conditions);
    this._percent = percent;
  }

  _getDiscountAmount(screening: { getMovieFee: () => Money }): Money {
    return screening.getMovieFee().times(this._percent);
  }
}
