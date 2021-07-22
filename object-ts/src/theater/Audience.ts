import Bag, { buyResult } from "./Bag";
import Ticket from "./Ticket";

export default class Audience {
  _bag: Bag

  constructor(bag: Bag){
    this._bag = bag;
  }

  buy(ticket: Ticket): buyResult{
    return this._bag.buy(ticket);
  }

  hasTicket(): boolean {
    return this._bag._ticket != null;
  }
}
