import Bag from "./Bag";
import Ticket from "./Ticket";

export type canPayResult = "have invitation" | "can pay" | "can not buy";

export default class Audience {
  _bag: Bag

  constructor(bag: Bag){
    this._bag = bag;
  }

  hasInvitationOrCanPay(fee: number): canPayResult {
    if (this._bag.hasInvitation()){ // calc
      return "have invitation";
    } else if (this._bag._amount > fee) {
      return "can pay";
    } else {
      return "can not buy";
    }
  }

  pay(fee: number): void {
    this._bag.minusAmount(fee); // effect
  }

  hasTicket(): boolean {
    return this._bag._ticket != null;
  }

  receiveTicket(ticket: Ticket){
    this._bag.setTicket(ticket);
  }
}
