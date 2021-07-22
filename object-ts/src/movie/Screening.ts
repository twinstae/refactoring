import Customer from "./Customer";
import Reservation from "./Reservation";
import Movie from "./Movie";
import Money from "./Money";

export default class Screening {
  _movie: Movie
  _sequence: number
  _whenScreened: Date

  constructor(
    movie: Movie,
    sequence: number,
    whenScreened: Date,
  ){
    this._movie = movie;
    this._sequence = sequence;
    this._whenScreened = whenScreened;
  }

  reserve(customer: Customer, audienceCount: number): Reservation {
    const fee = this._calculateFee(audienceCount);
    return new Reservation(customer, this, fee, audienceCount);
  }

  getStartTime(): Date {
    return this._whenScreened;
  }

  isSequence(sequence: number): boolean {
    return this._sequence == sequence;
  }

  getMovieFee(): Money {
    return this._movie.getFee();
  }

  _calculateFee(audienceCount: number): Money {
    return this._movie.calculateMovieFee({
      isSequence: this.isSequence,
      startTime: this.getStartTime(),
    }).times(audienceCount);
  }
}
