import Theater from './Theater';
import Audience from './Audience';
import Bag from './Bag';
import TicketSeller from './TicketSeller';
import TicketOffice from './TicketOffice';
import Ticket from './Ticket';
import { Invitation } from './Invitation';

describe('Theater는', () => {
  const 티켓_가격 = 35000;
  const 금고에_있던_돈 = 10000;
  const 지갑에_있던_돈 = 50000;

  const ticket = new Ticket(티켓_가격);

  function theater_factory(money: number, tickets: Ticket[]) {
    const ticketOffice = new TicketOffice(money, tickets);
    const ticketSeller = new TicketSeller(ticketOffice);
    return new Theater(ticketSeller);
  }

  const invitation: Invitation = { when: new Date(2020, 9 - 1, 13) };

  function audience_factory(money: number, invitation: Invitation | null) {
    const bag = new Bag(invitation, money);
    return new Audience(bag);
  }

  function 손님은_티켓을_받고_극장은_티켓을_준다(audience: Audience, theater: Theater) {
    test('손님은 티켓을 받는다', () => {
      expect(audience.hasTicket()).toBeTruthy();
    });

    test('극장은 티켓을 잃는다', () => {
      expect(theater._ticketSeller._ticketOffice._tickets).toEqual([]);
    });
  }

  describe('초대장을 가진 손님이 입장하면', () => {
    const theater = theater_factory(금고에_있던_돈, [ticket]);
    const audience_with_inv = audience_factory(지갑에_있던_돈, invitation);

    theater.enter(audience_with_inv);

    손님은_티켓을_받고_극장은_티켓을_준다(audience_with_inv, theater);

    test('손님의 돈은 그대로다', () => {
      expect(audience_with_inv._bag._amount).toBe(지갑에_있던_돈);
    });

    test('극장의 돈도 그대로다', () => {
      expect(theater._ticketSeller._ticketOffice._amount).toBe(금고에_있던_돈);
    });
  });

  describe('초대장은 없고, 돈만 가진 손님이 입장하면', () => {
    const theater = theater_factory(금고에_있던_돈, [ticket]);
    const audience_only_money = audience_factory(지갑에_있던_돈, null);

    theater.enter(audience_only_money);

    손님은_티켓을_받고_극장은_티켓을_준다(audience_only_money, theater);

    test('손님은 돈을 준다', () => {
      expect(audience_only_money._bag._amount).toBe(지갑에_있던_돈 - 티켓_가격);
    });

    test('극장은 돈을 받는다', () => {
      expect(theater._ticketSeller._ticketOffice._amount).toBe(금고에_있던_돈 + 티켓_가격);
    });
  });

  describe('돈도 없는 손님이 입장하면', () => {
    const theater = theater_factory(금고에_있던_돈, [ticket]);
    const audience_no_money = audience_factory(0, null);

    theater.enter(audience_no_money);

    test('손님은 티켓이 없다. ㅠㅠ', () => {
      expect(audience_no_money.hasTicket()).toBeFalsy();
    });
    test('극장은 티켓을 가지고 있다.', () => {
      expect(theater._ticketSeller._ticketOffice._tickets).toEqual([ticket]);
    });

    test('손님의 돈은 그대로다', () => {
      expect(audience_no_money._bag._amount).toBe(0);
    });

    test('극장의 돈도 그대로다', () => {
      expect(theater._ticketSeller._ticketOffice._amount).toBe(금고에_있던_돈);
    });
  });
});
