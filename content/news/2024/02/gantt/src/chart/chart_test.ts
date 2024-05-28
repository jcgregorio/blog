import { assert } from "https://deno.land/std@0.224.0/assert/assert.ts";
import { Validate } from "./chart.ts";
import { Chart } from "./chart.ts";

Deno.test("A default chart validates.", () => {
  const r = Validate(new Chart());
  assert(r.ok);
});
