import Bag from "./Bag";

export default class Audience {
  _bag: Bag

  constructor(bag: Bag){
    this._bag = bag;
  }
}
