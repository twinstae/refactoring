import TicketSeller from "./TicketSeller";
import Audience from "./Audience";

export default class Theater {
  _ticketSeller: TicketSeller

  constructor(ticketSeller: TicketSeller){
    this._ticketSeller = ticketSeller;
  }

  enter(audience: Audience): void {
    if (audience._bag.hasInvitation()){ // calc
      const ticket = this._ticketSeller._ticketOffice.getTicket(); // effect
      audience._bag.setTicket(ticket); // effect
    } else {
      const ticket = this._ticketSeller._ticketOffice.getTicket(); // effect
      
      // transaction
      audience._bag.minusAmount(ticket.getFee()); // effect
      this._ticketSeller._ticketOffice.plusAmount(ticket.getFee()); // effect
      audience._bag.setTicket(ticket); // effect
    }
  }
}
