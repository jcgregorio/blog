// url_test.ts
import { assertEquals } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { Triangular } from "./triangular.ts";

Deno.test("Test with simple case c=b.", () => {
  const t = new Triangular(0, 1, 1);
  assertEquals(0, t.sample(0));
  assertEquals(1, t.sample(1));
});
