import { Triangular } from "./triangular.ts"
import { Jacobian, Uncertainty } from "./jacobian.ts";
const t = new Triangular(1, 10, 3);

const histogram: number[] = new Array(10);
histogram.fill(0);

for (let i = 0; i < 1000; i++) {
    const s = t.sample(i / 1000);
    histogram[Math.floor(s)] += 1;
}

console.log("histogram:", histogram);


interface Sampler {
    sample(p: number): number;
}

const Quartiles = (s: Sampler): void => {
    console.log("quartiles: ", s.sample(0.25), s.sample(0.5), s.sample(0.75))
}


Quartiles( new Jacobian(5, Uncertainty.extreme));

Quartiles(new Jacobian(5, Uncertainty.low));
