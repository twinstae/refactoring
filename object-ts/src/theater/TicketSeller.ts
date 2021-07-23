import Ticket from './Ticket';
import TicketOffice from './TicketOffice';

export default class TicketSeller {
  _ticketOffice: TicketOffice;

  constructor(ticketOffice: TicketOffice) {
    this._ticketOffice = ticketOffice;
  }

  getLastTicket(): Ticket {
    return this._ticketOffice.getLastTicket();
  }

  process_selling(received_money: number) {
    this._ticketOffice.process_selling(received_money);
  }
}
