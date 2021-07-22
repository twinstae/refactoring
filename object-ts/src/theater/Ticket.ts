export default class Ticket {
  _fee: number

  constructor(fee: number){
    this._fee = fee;
  }

  getFee(): number {
    return this._fee;
  }
}
