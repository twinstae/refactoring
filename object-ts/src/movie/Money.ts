export default class Money {
  static ZERO: Money = Money.wons(0);

  _amount: BigInt;

  constructor(amount: BigInt) {
    this._amount = amount;
  }

  static wons(amount: number): Money {
    return new Money(BigInt(amount));
  }

  plus(money: Money): Money {
    return new Money(this._amount + money._amount);
  }

  minus(money: Money): Money {
    return new Money(this._amount - money._amount);
  }

  times(percent: number): Money {
    return new Money((this._amount * BigInt(percent * 100)) / BigInt(100));
  }

  isLessThan(other: Money): boolean {
    return this._amount < other._amount;
  }

  isGreaterThatOrEqual(other: Money) {
    return this._amount >= other._amount;
  }
}
