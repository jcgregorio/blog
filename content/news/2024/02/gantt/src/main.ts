import { Chart, Task, ComputeSlack, Validate } from "./chart/chart.ts";
import { InsertNewEmptyTaskAfterOp } from "./ops/ops.ts";

const C: Chart = {
  Vertices: [
    new Task("Start"),
    new Task("A", 10),
    new Task("B", 15),
    new Task("Finish"),
  ],
  Edges: [
    { i: 0, j: 1 },
    { i: 0, j: 2 },
    { i: 1, j: 3 },
    { i: 2, j: 3 },
  ],
};

console.log("Tasks on the critical path:", ComputeSlack(C));
console.log(
  "Tasks on the critical path for in the first quartile:",
  ComputeSlack(C, (t: Task) => t.durationModel.sample(t.duration, 0.25))
);

let c2 = new Chart();
const op = InsertNewEmptyTaskAfterOp(0);
let err = op.apply(c2);
console.log("Applying op: ", err);
const op2 = InsertNewEmptyTaskAfterOp(1);
err = op2.apply(c2);
console.log("Applying op2: ", err);
err = op2.inverse().apply(c2);
console.log("Applying op2.inverse: ", err);

// Ops that fail to apply revert applied ops.
err = InsertNewEmptyTaskAfterOp(99).apply(c2);
console.log("Applying op: ", err);
console.log(Validate(c2));

console.log(JSON.stringify(c2, null, "  "));
