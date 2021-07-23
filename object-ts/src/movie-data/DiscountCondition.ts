type DayOfWeek = '월' | '화' | '수' | '목' | '금' | '토' | '일';
const DayOfWeekArray: DayOfWeek[] = ['월', '화', '수', '목', '금', '토', '일'];

export function n_to_day_of_week(n: number): DayOfWeek {
  if (n >= 7) {
    throw Error(`${n}은 0~6 월~일 사이의 값이 아닙니다!`);
  }

  return DayOfWeekArray[n];
}

export enum DiscountCondtionType {
  SEQUENCE,
  PERIOD,
}

export type SequenceCondition = {
  conditionType: DiscountCondtionType.SEQUENCE;
  sequence: number;
};

function checkSequence(condition: SequenceCondition, sequence: number) {
  return condition.sequence == sequence;
}

export type PeriodCondition = {
  conditionType: DiscountCondtionType.PERIOD;
  dayOfWeek: DayOfWeek;
  startTime: Date;
  endTime: Date;
};

function checkPeriod(condition: PeriodCondition, startTime: Date): boolean {
  return (
    n_to_day_of_week(startTime.getDay()) == condition.dayOfWeek &&
    condition.startTime <= startTime &&
    condition.endTime >= startTime
  );
}

export type DiscountCondtion = SequenceCondition | PeriodCondition;

interface ScreeningDto {
  startTime: Date;
  sequence: number;
}

export function satisfiedCondition(screeningDto: ScreeningDto, condition: DiscountCondtion): boolean {
  const { startTime, sequence } = screeningDto;

  if (condition.conditionType == DiscountCondtionType.PERIOD) {
    return checkPeriod(condition, startTime);
  } else {
    return checkSequence(condition, sequence);
  }
}
