import Money from './Money';

describe('Money는', () => {
  test('더하기', () => {
    const other = Money.wons(500);
    const result = Money.wons(500).plus(other);
    expect(result._amount).toEqual(BigInt(1000));
  });
});
