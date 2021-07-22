import Money from "./Money";
import DiscountCondition, {NeverDiscountCondition, ScreeningDto} from "./DiscountCondition";

export default abstract class DiscountPolicy {
  _conditions = [];

  constructor(conditions: DiscountCondition[]){
    this._conditions = conditions;
  }

  calculateDiscountAmount(screeningDto: ScreeningDto): Money{
    const is_discountable = this._conditions.some(cond => cond.isSatisfiedBy(screeningDto));
    
    if (is_discountable){
      return this._getDiscountAmount(screeningDto)
    }
    return Money.ZERO;
  }

  abstract _getDiscountAmount(screening: ScreeningDto): Money;
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

  _getDiscountAmount(screeningDto: { fee: Money }): Money {
    return screeningDto.fee.times(this._percent);
  }
}
