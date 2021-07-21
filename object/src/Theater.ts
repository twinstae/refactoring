import TicketSeller from "./TicketSeller";
import Audience, { pay_result } from "./Audience";

export default class Theater {
  _ticketSeller: TicketSeller

  constructor(ticketSeller: TicketSeller){
    this._ticketSeller = ticketSeller;
  }

  enter(audience: Audience): void {
    const ticket = this._ticketSeller.getTicket(); // effect
    const ticket_fee = ticket.getFee();

    const result = audience.show_invitation_or_pay(ticket_fee);
    if (result == "payed"){
      this._ticketSeller.receiveMoney(ticket_fee); // effect
    }

    audience.receiveTicket(ticket); // effect
  }
}
