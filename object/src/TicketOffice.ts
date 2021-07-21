import Ticket from "./Ticket";

export default class TicketOffice {
  _amount: number
  _tickets: Ticket[]

  constructor(amount: number, tickets: Ticket[]){
    this._amount = amount;
    this._tickets = tickets;
  }

  // effect
  getTicket(): Ticket{
    return this._tickets.pop();
  }

  // effect
  minusAmount(value: number): void {
    this._amount -= value;
  }

  // effect
  plusAmount(value: number): void {
    this._amount += value;
  }
}
