import Ticket from "./Ticket";
import TicketOffice from "./TicketOffice";

export default class TicketSeller {
  _ticketOffice: TicketOffice

  constructor(ticketOffice: TicketOffice){
    this._ticketOffice = ticketOffice;
  }

  getTicket(): Ticket{
    return this._ticketOffice.getTicket()
  }

  receiveMoney(money: number){
    this._ticketOffice.plusAmount(money);
  }
}
