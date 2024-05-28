import { assert } from "https://deno.land/std@0.224.0/assert/assert.ts";
import { Validate } from "./chart.ts";
import { Chart } from "./chart.ts";
import { DirectedGraph } from "../dag/dag.ts";
import { assertFalse } from "https://deno.land/std@0.224.0/assert/assert_false.ts";

Deno.test("A directed graph validates:", () => {
  const G: DirectedGraph = {
    Vertices: [{}, {}, {}, {}],
    Edges: [
      { i: 0, j: 1 },
      { i: 0, j: 2 },
      { i: 1, j: 3 },
      { i: 2, j: 3 },
    ],
  };
  assert(Validate(G).ok);
});

Deno.test("A directed graph with a loop fails to validate:", () => {
  const GWithLoop: DirectedGraph = {
    Vertices: [{}, {}, {}, {}],
    Edges: [
      { i: 0, j: 1 },
      { i: 0, j: 2 },
      { i: 1, j: 3 },
      { i: 2, j: 3 },
      { i: 2, j: 0 },
    ],
  };
  assertFalse(Validate(GWithLoop).ok);
});

Deno.test("A default chart validates.", () => {
  const r = Validate(new Chart());
  assert(r.ok);
});
