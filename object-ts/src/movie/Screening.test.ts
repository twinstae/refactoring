import Screening from "./Screening";
import Movie from "./Movie";
import Customer from "./Customer";
import Money from "./Money";
import { AmountDiscountPolicy } from "./DiscountPolicy";
import { AlwaysDiscountCondition } from "./DiscountCondition";

describe("Screening", ()=>{
  describe("아이즈온미 30000원을 5000원 할인해서", ()=>{
    const discountPolicy = new AmountDiscountPolicy(Money.wons(5000), [AlwaysDiscountCondition]);
    const movie = new Movie("아이즈온미 더 무비", Money.wons(30000), discountPolicy);
    const whenScreened = new Date(2020, 6 -1, 10, 12);
    const screening = new Screening(movie, 4, whenScreened);

    describe("2명이 예매하면", ()=>{
      const customer = new Customer();
      const reservation = screening.reserve(customer, 2);

      test("5만원이다.", ()=>{
        expect(reservation._fee._amount).toBe(Money.wons(50000)._amount)// 30000 * 2
      })
    })
  })
})
