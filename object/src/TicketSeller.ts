import Ticket from "./Ticket";
import TicketOffice from "./TicketOffice";

export default class TicketSeller {
  _ticketOffice: TicketOffice

  constructor(ticketOffice: TicketOffice){
    this._ticketOffice = ticketOffice;
  }

  getTicket(): Ticket {
    return this._ticketOffice._tickets[this._ticketOffice._tickets.length - 1];
  }

  process_selling(received_money: number){
    this._receiveMoney(received_money);
    this._popTicket();
  }

  _popTicket(): void{
    this._ticketOffice.getTicket()
  }

  _receiveMoney(money: number){
    this._ticketOffice.plusAmount(money);
  }
}
