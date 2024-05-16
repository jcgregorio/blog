import { Result, ok, error } from "./result.ts";
import {
  Vertex,
  VertexIndices,
  DirectedEdge,
  Edges,
  DirectedGraph,
  edgesBySrcToMap,
  edgesByDstToMap,
} from "./dag/dag.ts";

import {
  depthFirstSearch,
  depthFirstSearchFromIndex,
  setOfVerticesWithNoIncomingEdge,
} from "./dag/algorithms/dfs.ts";

import { topologicalSort } from "./dag/algorithms/toposort.ts";

/** Simulates the expected distribution of durations.
 *
 *  Note that we can create quartiles from this by feeding in the values [0.25,
 *  0.5, 0.75].
 */
interface DurationModel {
  // Input is the task duration, and a number in the range [0,1] and is passed
  // into the inverse CDF for durations. Implementations should memoize the CDF
  // based on the passed in duration.
  sample(duration: number, p: number): number;

  // Serializes the Model to JSON. Note that it MUST serialize the class name of
  // the DurationModel implementation in the 'ctor' value of the returned
  // object. Unless that's not needed and we store the ctor as part of the
  // Chart?
  toJSON(key: string): any;
}

class DefaultDurationModel implements DurationModel {
  private lastDuration: number = -1;
  sample(d: number, p: number): number {
    return 1.0;
  }

  toJSON(key: string): any {
    return {};
  }
}

class PERTDuration {
  optimistic: number;
  pessimistic: number;
  private duration: number;
}

enum Uncertainty {
  low = 1.1,
  medium = 1.5,
  high = 2.0,
  extreme = 5.0,
}

class JacobianDuration {
  uncertainty: Uncertainty;
}

enum TaskState {
  unstarted = "unstarted",
  started = "started",
  complete = "complete",
}

/** The standard PERT slack calculation values. */
class Slack {
  earlyStart: number = 0;
  earlyFinish: number = 0;
  lateStart: number = 0;
  lateFinish: number = 0;
  slack: number = 0;
}

// Do we create sub-classes and then serialize separately? Or do we have a
// config about which type of DurationSampler is being used?
//
// We can use traditional optimistic/pessimistic value. Or Jacobian's
// uncertaintly multipliers [1.1, 1.5, 2, 5] and their inverses to generate an
// optimistic pessimistic.

/** Task is a Vertex with details about the Task to complete. */
class Task {
  constructor(
    name: string = "",
    duration: number = 0,
    durationModel: DurationModel | null = null
  ) {
    if (name === "") {
      this.name = "Task Name";
    } else {
      this.name = name;
    }
    this.duration = duration;
    this.durationModel = durationModel || new DefaultDurationModel();
  }

  name: string = "Task Name";

  // How long does this task take. Note this value is unitless, so it could be
  // seconds, days, or years.
  duration: number;

  durationModel: DurationModel;

  state: TaskState = TaskState.unstarted;

  // Recorded as the number of days from the Start Milestone.
  actualStart: number;

  // Recorded as the number of days from the Start Milestone.
  calculatedStart: number;

  // Having a non-zero value here would require that actualStart be populated.
  percentComplete: number;

  slack: Slack;
}

type Tasks = Task[];

/** A Chart is a DirectedGraph, but with Tasks for Vertices. */
class Chart {
  Vertices: Tasks = [new Task("Start"), new Task("Finish")];
  Edges: Edges = [];
}

type TopologicalOrder = VertexIndices;

type ValidateResult = Result<TopologicalOrder>;

/** Validates a DirectedGraph is a valid Chart. */
function Validate(g: DirectedGraph): ValidateResult {
  if (g.Vertices.length < 2) {
    return error(
      "Chart must contain at least two node, the start and finish tasks."
    );
  }

  const edgesByDst = edgesByDstToMap(g.Edges);
  const edgesBySrc = edgesBySrcToMap(g.Edges);

  // The first Vertex, T_0 aka the Start Milestone, must have 0 incoming edges.
  if (edgesByDst.get(0) !== undefined) {
    return error("The start node (0) has an incoming edge.");
  }

  // And only T_0 should have 0 incoming edges.
  for (let i = 1; i < g.Vertices.length; i++) {
    if (edgesByDst.get(i) === undefined) {
      return error(
        `Found node that isn't (0) that has no incoming edges: ${i}`
      );
    }
  }

  // The last Vertex, T_finish, the Finish Milestone, must have 0 outgoing edges.
  if (edgesBySrc.get(g.Vertices.length - 1) !== undefined) {
    return error(
      "The last node, which should be the Finish Milestone, has an outgoing edge."
    );
  }

  // And only T_finish should have 0 outgoing edges.
  for (let i = 0; i < g.Vertices.length - 1; i++) {
    if (edgesBySrc.get(i) === undefined) {
      return error(
        `Found node that isn't T_finish that has no outgoing edges: ${i}`
      );
    }
  }

  const numVertices = g.Vertices.length;
  // And all edges make sense, i.e. they all point to vertexes that exist.
  for (let i = 0; i < g.Edges.length; i++) {
    const element = g.Edges[i];
    if (
      element.i < 0 ||
      element.i >= numVertices ||
      element.j < 0 ||
      element.j >= numVertices
    ) {
      return error(`Edge ${element} points to a non-existent Vertex.`);
    }
  }

  // Now we confirm that we have a Directed Acyclic Graph, i.e. the graph has no
  // cycles by creating a topological sort starting at T_0
  // https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search
  const tsRet = topologicalSort(g);
  if (tsRet.hasCycles) {
    return error(`Chart has cycle: ${[...tsRet.cycle].join(", ")}`);
  }

  return ok(tsRet.order);
}

function ChartValidate(c: Chart): ValidateResult {
  let ret = Validate(c);
  if (!ret.ok) {
    return ret;
  }
  if (c.Vertices[0].duration !== 0) {
    return error(
      `Start Milestone must have duration of 0, instead got ${C.Vertices[0].duration}`
    );
  }
  if (c.Vertices[c.Vertices.length - 1].duration !== 0) {
    return error(
      `Finish Milestone must have duration of 0, instead got ${
        C.Vertices[C.Vertices.length - 1].duration
      }`
    );
  }
  return ret;
}

// Do some testing.

const G: DirectedGraph = {
  Vertices: [{}, {}, {}, {}],
  Edges: [
    { i: 0, j: 1 },
    { i: 0, j: 2 },
    { i: 1, j: 3 },
    { i: 2, j: 3 },
  ],
};

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

console.log("IsChart: new Chart()", Validate(new Chart()));
console.log("IsChart: G", Validate(G));
console.log("IsChart: GWithLoop", Validate(GWithLoop));

type TaskDuration = (t: Task) => number;

const defaultTaskDuration = (t: Task): number => {
  return t.duration;
};

type SlackResult = Result<Slack[]>;

// Calculate the slack for each Task in the Chart.
function ComputeSlack(
  c: Chart,
  taskDuration: TaskDuration = defaultTaskDuration
): SlackResult {
  // Create a Slack for each Task.
  const slacks: Slack[] = [];
  for (let i = 0; i < c.Vertices.length; i++) {
    slacks.push(new Slack());
  }

  const r = ChartValidate(c);
  if (!r.ok) {
    return error(r.error);
  }

  const edgesByDst = edgesByDstToMap(c.Edges);
  const edgesBySrc = edgesBySrcToMap(c.Edges);

  const topologicalOrder = r.value;

  // First go forward through the topological sort and find the early start for
  // each task, which is the max of all the predecessors early finish values.
  // Since we know the duration we can also compute the early finish.
  topologicalOrder.slice(1).forEach((vertexIndex: number) => {
    const task = c.Vertices[vertexIndex];
    const slack = slacks[vertexIndex];
    slack.earlyStart = Math.max(
      ...edgesByDst.get(vertexIndex)!.map((e: DirectedEdge): number => {
        const predecessorSlack = slacks[e.i];
        return predecessorSlack.earlyFinish;
      })
    );
    slack.earlyFinish = slack.earlyStart + taskDuration(task);
  });

  // Now backwards through the topological sort and find the late finish of each
  // task, which is the min of all the successor tasks late starts. Again since
  // we know the duration we can also compute the late start. Finally, since we
  // now have all the early/late and start/finish values we can now calcuate the
  // slack.
  topologicalOrder.reverse().forEach((vertexIndex: number) => {
    const task = c.Vertices[vertexIndex];
    const slack = slacks[vertexIndex];
    const successors = edgesBySrc.get(vertexIndex);
    if (!successors) {
      slack.lateFinish = slack.earlyFinish;
      slack.lateStart = slack.earlyStart;
    } else {
      slack.lateFinish = Math.min(
        ...edgesBySrc.get(vertexIndex)!.map((e: DirectedEdge): number => {
          const successorSlack = slacks[e.j];
          return successorSlack.lateStart;
        })
      );
      slack.lateStart = slack.lateFinish - taskDuration(task);
      slack.slack = slack.lateFinish - slack.earlyFinish;
    }
  });

  return ok(slacks);
}

// Operations on Charts. Note they are reversible, so we can have an 'undo' list.

// Also, some operations might have 'partials', i.e. return a list of valid
// options that can be passed to the operation. For example, adding a
// predecessor could list all the Tasks that would not form a loop, i.e. exclude
// all descendents, and the Task itself, from the list of options.
//
// * Change string value in a Task.
// * Change duration value in a Task.
// * Add predecessor to a Task.
// * Add successor to a Task.
// * Delete predecessor to a Task.
// * Delete successor to a Task.
// * Insert new empty Task after another Task.
// * Duplicate a Task.
// * Split a Task.
// * Delete a Task.

// Need Undo/Redo Stacks.
// These record the sub-ops for each large op. E.g. an insert task op is made
// of three sub-ops:
//    1. insert task into Vertices and renumber Edges
//    2. Add edge from Start to New Task
//    3. Add edge from New Task to Finish
//
// Each sub-op:
//    1. Records all the info it needs to work.
//    2. Can be "applied" to a Chart.
//    3. Can generate its inverse sub-op.

interface SubOp {
  // If the apply returns an error it is guaranteed no to have modified the
  // Chart.
  apply(c: Chart): Result<Chart>;

  inverse(): SubOp;
}

class Op {
  subOps: SubOp[] = [];

  constructor(subOps: SubOp[]) {
    this.subOps = subOps;
  }

  revertUpTo(c: Chart, index: number): Result<Chart> {
    const subOpsToRevert = this.subOps.slice(0, index).reverse();

    for (let i = 0; i < subOpsToRevert.length; i++) {
      const o = subOpsToRevert[i];
      const e = o.inverse().apply(c);
      if (!e.ok) {
        return e;
      }
      c = e.value;
    }
    return ok(c);
  }

  apply(c: Chart): Result<Chart> {
    for (let i = 0; i < this.subOps.length; i++) {
      const s = this.subOps[i];
      const e = s.apply(c);
      if (!e.ok) {
        // Revert all the SubOps applied to this point to get the Chart
        // back in a good place.
        const revertErr = this.revertUpTo(c, i);
        if (!revertErr.ok) {
          return revertErr;
        }
        return e;
      }
    }
    return ok(c);
  }

  inverse(): Op {
    const reversedInverted = this.subOps
      .slice()
      .reverse()
      .map((s: SubOp) => s.inverse());
    return new Op(reversedInverted);
  }
}

/** A value of -1 for j means the Finish Milestone. */
function DirectedEdgeForChart(
  i: number,
  j: number,
  c: Chart
): Result<DirectedEdge> {
  if (j === -1) {
    j = c.Vertices.length - 1;
  }
  if (i < 0 || i >= c.Vertices.length) {
    return error(
      `i index out of range: ${i} not in [0, ${c.Vertices.length - 1}]`
    );
  }
  if (j < 0 || j >= c.Vertices.length) {
    return error(
      `j index out of range: ${j} not in [0, ${c.Vertices.length - 1}]`
    );
  }
  if (i === j) {
    return error(`A Task can not depend on itself: ${i} === ${j}`);
  }
  return ok(new DirectedEdge(i, j));
}

class AddEdgeSubOp implements SubOp {
  i: number = 0;
  j: number = 0;

  constructor(i: number, j: number) {
    this.i = i;
    this.j = j;
  }

  apply(c: Chart): Result<Chart> {
    const e = DirectedEdgeForChart(this.i, this.j, c);
    if (!e.ok) {
      return e;
    }
    c.Edges.push(e.value);
    return ok(c);
  }

  inverse(): SubOp {
    return new RemoveEdgeSupOp(this.i, this.j);
  }
}

class RemoveEdgeSupOp implements SubOp {
  i: number = 0;
  j: number = 0;

  constructor(i: number, j: number) {
    this.i = i;
    this.j = j;
  }

  apply(c: Chart): Result<Chart> {
    const e = DirectedEdgeForChart(this.i, this.j, c);
    if (!e.ok) {
      return e;
    }
    c.Edges = c.Edges.filter((v: DirectedEdge): boolean => {
      if (v.i === e.value.i && v.j === e.value.j) {
        return false;
      }
      return true;
    });
    return ok(c);
  }

  inverse(): SubOp {
    return new AddEdgeSubOp(this.i, this.j);
  }
}

class AddTaskAfterSubOp implements SubOp {
  index: number = 0;

  constructor(index: number) {
    this.index = index;
  }

  apply(c: Chart): Result<Chart> {
    if (this.index < 0 || this.index > c.Vertices.length - 2) {
      return error(
        `${this.index} is not in range [0, ${c.Vertices.length - 2}]`
      );
    }
    c.Vertices.splice(this.index + 1, 0, new Task());

    // Update Edges.
    for (let i = 0; i < c.Edges.length; i++) {
      const edge = c.Edges[i];
      if (edge.i >= this.index + 1) {
        edge.i++;
      }
      if (edge.j >= this.index + 1) {
        edge.j++;
      }
    }
    return ok(c);
  }

  inverse(): SubOp {
    return new DeleteTaskAfterSubOp(this.index);
  }
}

class DeleteTaskAfterSubOp implements SubOp {
  index: number = 0;

  constructor(index: number) {
    this.index = index;
  }

  apply(c: Chart): Result<Chart> {
    if (this.index < 0 || this.index > c.Vertices.length - 2) {
      return error(
        `${this.index} is not in range [0, ${c.Vertices.length - 2}]`
      );
    }
    c.Vertices.splice(this.index + 1, 1);

    // Update Edges.
    for (let i = 0; i < c.Edges.length; i++) {
      const edge = c.Edges[i];
      if (edge.i >= this.index + 1) {
        edge.i--;
      }
      if (edge.j >= this.index + 1) {
        edge.j--;
      }
    }

    return ok(c);
  }

  inverse(): SubOp {
    return new AddTaskAfterSubOp(this.index);
  }
}

function InsertNewEmptyTaskAfterOp(index: number): Op {
  return new Op([
    new AddTaskAfterSubOp(index),
    new AddEdgeSubOp(0, index + 1),
    new AddEdgeSubOp(index + 1, -1),
  ]);
}

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
