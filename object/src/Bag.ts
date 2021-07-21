import { Invitation } from "./Invitation";
import Ticket from "./Ticket";

export default class Bag {
  _invitation: Invitation
  _amount: number
  _ticket: Ticket | null

  constructor(invitation: Invitation, amount: number){
    this._invitation = invitation;
    this._amount = amount;
    this._ticket = null;
  }

  ofAmount(amount: number){
    return new Bag(null, amount);
  }

  hasInvitation(): boolean {
    return this._invitation != null;
  }

  minusAmount(value: number): void {
    this._amount -= value;
  }

  setTicket(ticket: Ticket): void{
    this._ticket = ticket;
  }
}
