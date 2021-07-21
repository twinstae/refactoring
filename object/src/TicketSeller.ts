import Ticket from "./Ticket";
import TicketOffice from "./TicketOffice";

export default class TicketSeller {
  _ticketOffice: TicketOffice

  constructor(ticketOffice: TicketOffice){
    this._ticketOffice = ticketOffice;
  }

  getTicketFee(): number {
    return this._ticketOffice._tickets[this._ticketOffice._tickets.length - 1].getFee()
  }

  popTicket(): Ticket{
    return this._ticketOffice.getTicket()
  }

  receiveMoney(money: number){
    this._ticketOffice.plusAmount(money);
  }
}
