import Money from './Money';

export interface ScreeningDto {
  startTime: Date;
  isSequence: (sequence: number) => boolean;
  fee: Money;
}

export default interface DiscountCondition {
  isSatisfiedBy(screening: ScreeningDto): boolean;
}

export const AlwaysDiscountCondition = { isSatisfiedBy: (_: ScreeningDto) => true };
export const NeverDiscountCondition = { isSatisfiedBy: (_: ScreeningDto) => false };

export class SequenceCondition implements DiscountCondition {
  _sequence: number;

  constructor(sequence: number) {
    this._sequence = sequence;
  }

  isSatisfiedBy(screening: { isSequence: (sequence: number) => boolean }): boolean {
    return screening.isSequence(this._sequence);
  }
}

type DayOfWeek = '월' | '화' | '수' | '목' | '금' | '토' | '일';

function n_to_day_of_week(n: number) {
  if (n >= 7) {
    throw Error(`${n}은 0~6 월~일 사이의 값이 아닙니다!`);
  }

  return ['월', '화', '수', '목', '금', '토', '일'][n];
}

export class PeriodCondition implements DiscountCondition {
  _dayOfWeek: DayOfWeek;
  _startTime: Date;
  _endTime: Date;

  constructor(dayOfWeek: DayOfWeek, startTime: Date, endTime: Date) {
    this._dayOfWeek = dayOfWeek;
    this._startTime = startTime;
    this._endTime = endTime;
  }

  isSatisfiedBy({ startTime }): boolean {
    const dayOfWeek = n_to_day_of_week(startTime.getDay());

    return dayOfWeek == this._dayOfWeek && this._startTime < startTime && startTime < this._endTime;
  }
}
