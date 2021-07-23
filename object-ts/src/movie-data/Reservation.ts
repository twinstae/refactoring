import Money from '../movie/Money';
import { Customer } from './Customer';
import { Screening } from './Screening';

export type Reservation = {
  customer: Customer;
  screening: Screening;
  fee: Money;
  audienceCount: number;
};
