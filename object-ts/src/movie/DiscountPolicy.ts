import Money from "./Money";
import Screening from "./Screening";

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

  _getDiscountAmount(_: Screening): Money {
    return this._discountAmount;
  }
}


export class PercentDiscountPolicy extends DiscountPolicy {
  _percent: number;

  constructor(percent: number, conditions: DiscountCondition[]){
    super(conditions);
    this._percent = percent;
  }

  _getDiscountAmount(screening: Screening): Money {
    return screening.getMovieFee().times(this._percent);
  }
}


interface DiscountCondition {
  isSatisfiedBy(screening: Screening): boolean
}

export class SequenceCondition implements DiscountCondition {
  _sequence: number

  constructor(sequence: number){
    this._sequence = sequence;
  }

  isSatisfiedBy(screening: Screening): boolean{
    return screening.isSequence(this._sequence);
  }
}

type DayOfWeek = "월" | "화" | "수" | "목" | "금" | "토" | "일";

function n_to_day_of_week(n: number){
  if (n >= 7) {
    throw Error(`${n}은 0~6 월~일 사이의 값이 아닙니다!`);
  }

  return ["월", "화", "수", "목", "금", "토", "일"][n];
}

export class PeriodCondition implements DiscountCondition {
  _dayOfWeek: DayOfWeek
  _startTime: Date
  _endTime: Date

  constructor(dayOfWeek: DayOfWeek, startTime: Date, endTime: Date){
    this._dayOfWeek = dayOfWeek;
    this._startTime = startTime;
    this._endTime = endTime;
  }

  isSatisfiedBy(screening: Screening): boolean {
    const startTime = screening.getStartTime();
    const dayOfWeek = n_to_day_of_week(startTime.getDay());

    return dayOfWeek == this._dayOfWeek
      && this._startTime < startTime && startTime < this._endTime
  }
}

