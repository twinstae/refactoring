import { Invitation } from './Invitation';
import Ticket from './Ticket';

export type buyResult = 'have invitation' | 'paid' | 'can not buy';

export default class Bag {
  _invitation: Invitation;
  _amount: number;
  _ticket: Ticket | null;

  constructor(invitation: Invitation, amount: number) {
    this._invitation = invitation;
    this._amount = amount;
    this._ticket = null;
  }

  ofAmount(amount: number) {
    return new Bag(null, amount);
  }

  buy(ticket: Ticket): buyResult {
    const ticket_fee = ticket.getFee();
    const canBuy = this._canBuy(ticket_fee);

    if (canBuy == 'can not buy') {
      return 'can not buy';
    }

    if (canBuy == 'paid') {
      this._minusAmount(ticket_fee); // effect
    }
    this._setTicket(ticket); // effect

    return canBuy;
  }

  _hasInvitation(): boolean {
    return this._invitation != null;
  }

  _canBuy(fee: number): buyResult {
    if (this._hasInvitation()) {
      // calc
      return 'have invitation';
    } else if (this._amount > fee) {
      return 'paid';
    } else {
      return 'can not buy';
    }
  }

  _minusAmount(value: number): void {
    this._amount -= value;
  }

  _setTicket(ticket: Ticket): void {
    this._ticket = ticket;
  }
}
