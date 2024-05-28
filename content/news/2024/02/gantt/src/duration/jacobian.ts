import { Triangular } from "../stats/cdf/triangular/triangular.ts";

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
