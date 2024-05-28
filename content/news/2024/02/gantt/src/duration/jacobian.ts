import { Triangular } from "../stats/cdf/triangular/triangular.ts";

/**
 * Uncertainty is a measure of how uncertain you are of a tasks duration.
 *
 * These names and values are taken from:
 *
 *    https://jacobian.org/2021/may/25/my-estimation-technique/
 */
export enum Uncertainty {
  low = 1.1,
  moderate = 1.5,
  high = 2.0,
  extreme = 5.0,
}

export class JacobianDuration {
  private lastDuration: number = -1;
  private uncertainty: Uncertainty;
  private triangular: Triangular | null = null;

  constructor(uncertainty: Uncertainty) {
    this.uncertainty = uncertainty;
  }

  sample(duration: number, p: number): number {
    if (this.lastDuration !== duration || !this.triangular) {
      this.triangular = new Triangular(
        duration / this.uncertainty,
        duration * this.uncertainty,
        duration
      );
    }
    return this.triangular.sample(p);
  }

  toJSON(_key: string): object {
    return {
      ctor: "JacobianDuration",
      uncertainty: this.uncertainty,
    };
  }
}
