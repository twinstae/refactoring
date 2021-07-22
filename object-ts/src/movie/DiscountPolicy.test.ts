import {
  AmountDiscountPolicy,
  NoneDiscountPolicy,
  PercentDiscountPolicy,
} from "./DiscountPolicy";
import {
  NeverDiscountCondition,
  AlwaysDiscountCondition,
} from "./DiscountCondition";
import Money from "./Money";

function expectMoneyEqual(a: Money, b: Money){
  expect(a._amount).toEqual(b._amount);
}

describe("DiscountPolicy", ()=>{
  describe("AmountDiscountPolicy", ()=>{
    test("할인액은 일정하다.", ()=>{
      const policy = new AmountDiscountPolicy(
        Money.wons(5000),
        [AlwaysDiscountCondition]
      );

      const discountAmount = policy.calculateDiscountAmount(null);
      expectMoneyEqual(discountAmount, Money.wons(5000));
    })

    test("조건에 맞지 않으면, 할인되지 않는다.", ()=>{
      const policy = new AmountDiscountPolicy(
        Money.wons(5000),
        [NeverDiscountCondition] // <- 절대 통과하지 못함.
      );

      const discountAmount = policy.calculateDiscountAmount(null);
      expectMoneyEqual(discountAmount, Money.ZERO);
    })
  })

  describe("PercentDiscountPolicy", ()=>{
    test("percent로 0.5를 넣으면, 50% 할인이 된다", ()=>{
      const policy = new PercentDiscountPolicy(
        0.5,
        [AlwaysDiscountCondition]
      );

      const discountAmount = policy._getDiscountAmount({
        getMovieFee: () => Money.wons(39000) 
      })
      
      expectMoneyEqual(discountAmount, Money.wons(39000 * 0.5));
    })
  })

  describe("NoneDiscountPolicy", ()=>{
    test("할인액은 0원 = ZERO 다.", ()=>{
      const discountAmount = NoneDiscountPolicy.calculateDiscountAmount(null);
      expectMoneyEqual(discountAmount, Money.ZERO);
    })
  })
})
