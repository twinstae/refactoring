import Bag from "./Bag";
import Ticket from "./Ticket";

export type pay_result = "invitation" | "payed";

export default class Audience {
  _bag: Bag

  constructor(bag: Bag){
    this._bag = bag;
  }

  show_invitation_or_pay(fee: number): pay_result {
    if (this._bag.hasInvitation()){ // calc
      return "invitation"
    } else { 
      this._bag.minusAmount(fee); // effect
      return "payed"
    }
  }

  receiveTicket(ticket: Ticket){
    this._bag.setTicket(ticket);
  }
}
