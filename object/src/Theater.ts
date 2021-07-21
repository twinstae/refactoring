import TicketSeller from "./TicketSeller";
import Audience, { pay_result } from "./Audience";

export default class Theater {
  _ticketSeller: TicketSeller

  constructor(ticketSeller: TicketSeller){
    this._ticketSeller = ticketSeller;
  }

  enter(audience: Audience): boolean {
    const ticket_fee = this._ticketSeller.getTicketFee(); // calc

    const result = audience.hasInvitationOrCanPay(ticket_fee); // calc
    if (result == "can not buy"){
      return false;
    }

    if (result == "can pay"){
      audience.pay(ticket_fee);
      this._ticketSeller.receiveMoney(ticket_fee); // effect
    }

    const ticket = this._ticketSeller.popTicket(); // effect
    audience.receiveTicket(ticket); // effect
    return true;
  }
}
