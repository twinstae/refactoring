import Money from "../movie/Money";
import Screening from "./Screening";

export default class Reservation {
  customer: Customer
  screening: Screening
  fee: Money
  audienceCount: number


  constructor(
    customer: Customer,
    screening: Screening,
    fee: Money,
    audienceCount: number
  ){
    this.customer = customer;
    this.screening = screening;
    this.fee = fee;
    this.audienceCount = audienceCount;
  }
}
