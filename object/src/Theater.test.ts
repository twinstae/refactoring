import Theater from "./Theater";
import Audience from "./Audience";
import Bag from "./Bag";
import TicketSeller from "./TicketSeller";
import TicketOffice from "./TicketOffice";
import Ticket from "./Ticket";
import { Invitation } from "./Invitation";

describe("Theater는", ()=>{
  const 티켓_가격 = 35000;
  const 금고에_있던_돈 = 10000;
  const 지갑에_있던_돈 = 50000;

  describe("초대장을 가진 손님이 입장하면", ()=>{
    const oneiricTicket = new Ticket(티켓_가격);
    const ticketOffice = new TicketOffice(금고에_있던_돈, [oneiricTicket]);
    const interparkSeller = new TicketSeller(ticketOffice);
    const oneiricTheater = new Theater(interparkSeller);

    const invitation: Invitation = { when: new Date(2020, 9-1, 13) }
    const bag = new Bag(invitation, 지갑에_있던_돈);
    const audience_with_inv = new Audience(bag);
    
    oneiricTheater.enter(audience_with_inv);

    test("손님은 티켓을 받는다", ()=>{
      expect(audience_with_inv._bag._ticket).toBe(oneiricTicket)
    })

    test("극장은 티켓을 잃는다", ()=>{
      expect(oneiricTheater._ticketSeller._ticketOffice._tickets).toEqual([]);
    })

    test("손님의 돈은 그대로다", ()=>{
      expect(audience_with_inv._bag._amount).toBe(지갑에_있던_돈);
    })

    test("극장의 돈도 그대로다", ()=>{
      expect(oneiricTheater._ticketSeller._ticketOffice._amount).toBe(금고에_있던_돈);
    })
  })

  describe("초대장이 없는 손님이 입장하면", ()=>{
    const oneiricTicket = new Ticket(티켓_가격);
    const ticketOffice = new TicketOffice(10000, [oneiricTicket]);
    const interparkSeller = new TicketSeller(ticketOffice);
    const oneiricTheater = new Theater(interparkSeller);

    const bag = new Bag(null, 지갑에_있던_돈);
    const audience_only_money = new Audience(bag);
    
    oneiricTheater.enter(audience_only_money);

    test("손님은 티켓을 받는다", ()=>{
      expect(audience_only_money._bag._ticket).toBe(oneiricTicket);
    });
    test("극장은 티켓을 준다", ()=>{
      expect(oneiricTheater._ticketSeller._ticketOffice._tickets).toEqual([]);
    })

    test("손님은 돈을 준다", ()=>{
      expect(audience_only_money._bag._amount).toBe(지갑에_있던_돈 - 티켓_가격);
    })

    test("극장은 돈을 받는다", ()=>{
      expect(oneiricTheater._ticketSeller._ticketOffice._amount).toBe(금고에_있던_돈 + 티켓_가격);
    })
  })
})

