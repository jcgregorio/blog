/**
 * Triangular is the inverse Cumulative Density Function (CDF) for the
 * triangular distribution.
 *
 * https://en.wikipedia.org/wiki/Triangular_distribution#Generating_random_variates
 *
 * The inverse of the CDF is useful for generating samples from the
 * distribution, i.e. passing in values from the uniform distribution [0, 1]
 * will produce sample that look like they come from the triangular
 * distribution.
 *
 *
 */

export class Triangular {
  private a: number;
  private b: number;
  private c: number;
  private F_c: number;

  /**  The triangular distribution is a continuous probability distribution with
  lower limit `a`, upper limit `b`, and mode `c`, where a < b and a ≤ c ≤ b. */
  constructor(a: number, b: number, c: number) {
    this.a = a;
    this.b = b;
    this.c = c;

    // F_c is the cutoff in the domain where we switch between the two halves of
    // the triangle.
    this.F_c = (c - a) / (b - a);
  }

  /**  Produce a sample from the triangular distribution. The value of 'p'
   should be in [0, 1.0]. */
  sample(p: number): number {
    if (p < 0) {
      return 0;
    } else if (p > 1.0) {
      return 1.0;
    } else if (p < this.F_c) {
      return this.a + Math.sqrt(p * (this.b - this.a) * (this.c - this.a));
    } else {
      return (
        this.b - Math.sqrt((1 - p) * (this.b - this.a) * (this.b - this.c))
      );
    }
  }
}
