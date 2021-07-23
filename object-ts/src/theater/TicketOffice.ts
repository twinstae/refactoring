import Ticket from './Ticket';

export default class TicketOffice {
  _amount: number;
  _tickets: Ticket[];

  constructor(amount: number, tickets: Ticket[]) {
    this._amount = amount;
    this._tickets = tickets;
  }

  getLastTicket(): Ticket {
    return this._tickets[this._tickets.length - 1];
  }

  process_selling(received_money: number): void {
    this._plusAmount(received_money);
    this._popTicket();
  }

  // effect
  _popTicket(): void {
    this._tickets.pop();
  }

  // effect
  _plusAmount(value: number): void {
    this._amount += value;
  }
}
