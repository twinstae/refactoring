import TicketOffice from "./TicketOffice";

export default class TicketSeller {
  _ticketOffice: TicketOffice

  constructor(ticketOffice: TicketOffice){
    this._ticketOffice = ticketOffice;
  }
}
