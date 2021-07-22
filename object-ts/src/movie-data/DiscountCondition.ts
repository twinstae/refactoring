type DayOfWeek = "월" | "화" | "수" | "목" | "금" | "토" | "일";

export function n_to_day_of_week(n: number){
  if (n >= 7) {
    throw Error(`${n}은 0~6 월~일 사이의 값이 아닙니다!`);
  }

  return ["월", "화", "수", "목", "금", "토", "일"][n];
}
export enum DiscountCondtionType {
  SEQUENCE,
  PERIOD,
}

export default class DiscountCondtion {
  conditionType: DiscountCondtionType
  sequence: number
  dayOfWeek: DayOfWeek
  startTime: Date
  endTime: Date

  constructor(
    conditionType: DiscountCondtionType,
    sequence: number,
    dayOfWeek: DayOfWeek,
    startTime: Date,
    endTime: Date
  ){
    this.conditionType = conditionType;
    this.sequence = sequence;
    this.dayOfWeek = dayOfWeek;
    this.startTime = startTime;
    this.endTime = endTime;
  }
}


export const satisfiedCondition = ({ startTime, sequence}, condition: DiscountCondtion)=>{
  if (condition.conditionType == DiscountCondtionType.PERIOD){
    return n_to_day_of_week(startTime.getDay()) == condition.dayOfWeek
      && condition.startTime <= startTime
      && condition.endTime >= startTime;
  } else {
    return condition.sequence == sequence;
  }
};
