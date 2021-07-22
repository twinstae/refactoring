import {
  DiscountCondtionType,
  PeriodCondition,
  satisfiedCondition,
  n_to_day_of_week,
} from "./DiscountCondition"

describe("checkPeriod", ()=>{

  const 요일 = n_to_day_of_week(new Date(2021,7,21).getDay())

  const periodCondition: PeriodCondition = {
    conditionType: DiscountCondtionType.PERIOD,
    dayOfWeek: 요일,
    startTime: new Date(2021, 7, 21, 12, 30),
    endTime: new Date(2021, 7, 21, 16, 0)
  }

  // 할인 기간 21일 12시 30분 부터 21일 16시 0분 까지
  // 테스트명 날짜 시간 분 예상 결과
  type dataRow = [string, number, number, number, boolean];
  const data: dataRow[] = [
    ["하루 전" , 20, 13,  0, false],
    ["직전"    , 21, 12, 29, false],
    ["시작"    , 21, 12, 30, true ],
    ["도중"    , 21, 14,  0, true ],
    ["끝"      , 21, 16,  0, true ],
    ["직후"    , 21, 16,  1, false],
    ["하루 뒤,", 22, 13,  0, false],
  ];

  data.forEach(([ message, date, hours, minutes, expected ])=>{
    const dto = {
      startTime: new Date(2021, 7, date, hours, minutes),
      sequence: null,
    }
    test(`${dto.startTime.toLocaleString("ko")} ${expected ? "할인O" : "할인X"} ${message}` , ()=>{
      expect(satisfiedCondition(dto, periodCondition)).toBe(expected)
    });
  })
})
