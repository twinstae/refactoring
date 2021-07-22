import Movie, { calculateMovieFee } from "./Movie";

export default class Screening {
  movie: Movie
  sequence: number
  whenScreened: Date

  constructor(
    movie: Movie,
    sequence: number,
    whenScreened: Date, 
  ){
    this.movie = movie;
    this.sequence = sequence;
    this.whenScreened = whenScreened;
  }
}

export function calculateFee(screening: Screening){
  const screeningDto = { startTime: screening.whenScreened, sequence: screening.sequence };
  return calculateMovieFee(screening.movie, screeningDto);
}
