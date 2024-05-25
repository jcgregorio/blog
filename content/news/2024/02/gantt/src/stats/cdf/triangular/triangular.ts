/**
 * https://en.wikipedia.org/wiki/Triangular_distribution#Generating_random_variates
 */

export class Triangular {
    a: number;
    b: number;
    c: number;
    F_c: number;

    constructor(a, b, c: number) {
        this.a = a;
        this.b = b;
        this.c = c;
        this.F_c = (c - a) / (b - a);
    }

    sample(p: number): number {
        if (p < this.F_c) {
            return this.a + Math.sqrt(p * (this.b - this.a) * (this.c - this.a));
        } else {
            return this.b - Math.sqrt((1 - p) * (this.b - this.a) * (this.b - this.c))
        }
    }
}