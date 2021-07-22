import { Movie, calculateMovieFee } from "./Movie";

export type Screening = {
  movie: Movie
  sequence: number
  whenScreened: Date
}

export function calculateFee(screening: Screening){
  const screeningDto = {
    startTime: screening.whenScreened,
    sequence: screening.sequence
  };

  return calculateMovieFee(screening.movie, screeningDto);
}
