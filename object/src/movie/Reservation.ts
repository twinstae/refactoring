import Screening from "./Screening";
import Customer from "./Customer";
import Money from "./Money";

export default class Reservation {
  _customer: Customer
  _screening: Screening
  _fee: Money
  _audienceCount: number

  constructor(customer: Customer, screening: Screening, fee: Money, audienceCount: number){
    this._customer = customer;
    this._screening = screening;
    this._fee = fee;
    this._audienceCount = audienceCount;
  }
}
