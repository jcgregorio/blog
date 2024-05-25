// url_test.ts
import { assertEquals } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { Triangular } from "./triangular.ts";
import { assertAlmostEquals } from "https://deno.land/std@0.224.0/assert/assert_almost_equals.ts";

Deno.test("Test with simple case c=b.", () => {
  const t = new Triangular(0, 1, 1);
  assertEquals(0, t.sample(0));
  assertAlmostEquals(Math.SQRT2 / 2, t.sample(0.5));
  assertEquals(1, t.sample(1));
});

Deno.test("Test with simple case c=a.", () => {
  const t = new Triangular(0, 1, 0);
  assertEquals(0, t.sample(0));
  assertAlmostEquals(1 - Math.SQRT2 / 2, t.sample(0.5));
  assertEquals(1, t.sample(1));
});
