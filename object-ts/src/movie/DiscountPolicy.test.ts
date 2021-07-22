import { AmountDiscountPolicy, PercentDiscountPolicy } from "./DiscountPolicy"
import Money from "./Money";

const AlwaysDiscountCondition = { isSatisfiedBy: (_) => true  };
const NeverDiscountCondition  = { isSatisfiedBy: (_) => false };
describe("DiscountPolicy", ()=>{
  describe("AmountDiscountPolicy", ()=>{
    test("할인액은 일정하다.", ()=>{
      const policy = new AmountDiscountPolicy(
        Money.wons(5000),
        [AlwaysDiscountCondition]
      );

      const discountAmount = policy.calculateDiscountAmount(null);
      expect(discountAmount._amount).toBe(BigInt(5000))
    })

    test("조건에 맞지 않으면, 할인되지 않는다.", ()=>{
      const policy = new AmountDiscountPolicy(
        Money.wons(5000),
        [NeverDiscountCondition] // <- 절대 통과하지 못함.
      );

      const discountAmount = policy.calculateDiscountAmount(null);
      expect(discountAmount._amount).toEqual(Money.ZERO._amount);
    })
  })

  describe("PercentDiscountPolicy", ()=>{
    test("percent로 0.5를 넣으면, 50% 할인이 된다", ()=>{
      const policy = new PercentDiscountPolicy(
        0.5,
        [AlwaysDiscountCondition]
      );

      const discountAmount = policy.calculateDiscountAmount({
        getMovieFee: () => Money.wons(39000)
      })

      expect(discountAmount._amount).toBe(BigInt(39000 * 0.5));
    })
  })
})
