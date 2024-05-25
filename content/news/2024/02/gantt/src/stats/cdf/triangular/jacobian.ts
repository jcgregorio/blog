import { Triangular } from "./triangular.ts";

export enum Uncertainty {
  low = 1.1,
  moderate = 1.5,
  high = 2.0,
  extreme = 5.0,
}

export class Jacobian {
  private triangular: Triangular;
  constructor(expected: number, uncertainty: Uncertainty) {
    this.triangular = new Triangular(
      expected / uncertainty,
      expected * uncertainty,
      expected
    );
  }

  sample(p: number): number {
    return this.triangular.sample(p);
  }
}
