import TicketSeller from "./TicketSeller";
import Audience from "./Audience";


export default class Theater {
  _ticketSeller: TicketSeller

  constructor(ticketSeller: TicketSeller){
    this._ticketSeller = ticketSeller;
  }

  enter(audience: Audience): boolean {
    const ticket = this._ticketSeller.getLastTicket(); // calc

    const result = audience.buy(ticket); // effect
    if (result == "can not buy"){
      return false;
    }
    
    const received_money = result == "paid" ? ticket.getFee() : 0;
    this._ticketSeller.process_selling(received_money); // calc

    return true;
  }
}
