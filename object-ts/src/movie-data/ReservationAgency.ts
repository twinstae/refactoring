import { Customer } from './Customer';
import { Reservation } from './Reservation';
import { Screening, calculateFee } from './Screening';

export default function reserve(screening: Screening, customer: Customer, audienceCount: number): Reservation {
  return {
    customer,
    screening,
    fee: calculateFee(screening),
    audienceCount,
  };
}
