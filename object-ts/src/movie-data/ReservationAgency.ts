import Customer from "./Customer";
import Reservation from "./Reservation";
import Screening, {calculateFee} from "./Screening";

export default function reserve(screening: Screening, customer: Customer, audienceCount: number){
  return new Reservation(
    customer,
    screening,
    calculateFee(screening),
    audienceCount);
}

