import Screening from "./Screening";
import Movie from "./Movie";
import Customer from "./Customer";
import Money from "./Money";

describe("Screening", ()=>{
  const discountPolicy = {
    conditions: [],
    calculateDiscountAmount: (screening)=> Money.wons(0)
  };

  const movie = new Movie("아이즈온미 더 무비", 60, Money.wons(30000), discountPolicy);
  const whenScreened = new Date(2020, 6 -1, 10, 12);
  const screening = new Screening(movie, 4, whenScreened);

  describe("할인 없는 영화를", ()=>{
    describe("2명이 reserve하면", ()=>{
      const customer = new Customer();
      const reservation = screening.reserve(customer, 2);
      test("원래 2명 예매 가격 그대로", ()=>{
        expect(reservation._fee._amount).toBe(BigInt(60000))// 30000 * 2
      })
    })
  })
})
