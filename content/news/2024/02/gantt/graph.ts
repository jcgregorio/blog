/** One vertex of a graph. */
type Vertex = {};

/** Every Vertex in a graph. */
type Vertices = Vertex[];

/** A subset of Vertices referred to by their index number. */
type VertexIndices = number[];

/** One edge of a graph, which is a directed connection from the i'th Vertex to
the j'th Vertex, where the Vertex is stored in a Vertices.
 */
class DirectedEdge {
  constructor(i: number, j: number) {
    this.i = i;
    this.j = j;
  }

  i: number = 0;
  j: number = 0;
}

/** Every Egde in a graph. */
type Edges = DirectedEdge[];

/** A graph is just a collection of Vertices and Edges between those vertices. */
type DirectedGraph = {
  Vertices: Vertices;
  Edges: Edges;
};

/**
 Groups the Edges by their `i` value.

 @param edges - All the Eges in a DirectedGraph.
 @returns A map from the Vertex index to all the Edges that start at
   at that Vertex index.
 */
const edgesBySrcToMap = (edges: Edges): Map<number, Edges> => {
  const ret = new Map<number, Edges>();

  edges.forEach((e: DirectedEdge) => {
    const arr = ret.get(e.i) || [];
    arr.push(e);
    ret.set(e.i, arr);
  });

  return ret;
};

/**
 Groups the Edges by their `j` value.

 @param edges - All the Edges in a DirectedGraph.
 @returns A map from the Vertex index to all the Edges that end at
   at that Vertex index.
 */

const edgesByDstToMap = (edges: Edges): Map<number, Edges> => {
  const ret = new Map<number, Edges>();

  edges.forEach((e: DirectedEdge) => {
    const arr = ret.get(e.j) || [];
    arr.push(e);
    ret.set(e.j, arr);
  });

  return ret;
};

/** A function that can be applied to a Vertex, used in later functions like
Depth First Search to do work on every Vertex in a DirectedGraph.
 */
type vertexFunction = (v: Vertex, index: number) => boolean;

/** Returns teh index of all Vertices that have no incoming edge.
 */
const SetOfVerticesWithNoIncomingEdge = (g: DirectedGraph): VertexIndices => {
  const nodesWithIncomingEdges = edgesByDstToMap(g.Edges);
  const ret: VertexIndices = [];
  G.Vertices.forEach((_: Vertex, i: number) => {
    if (!nodesWithIncomingEdges.has(i)) {
      ret.push(i);
    }
  });
  return ret;
};

/** Descends the graph in Depth First Search and applies the function `f` to
each node.
 */
const DFS = (g: DirectedGraph, f: vertexFunction) => {
  SetOfVerticesWithNoIncomingEdge(g).forEach((value: Vertex, index: number) => {
    DFSFromIndex(g, index, f);
  });
};

/** Depth First Search starting at Vertex `start_index`. */
const DFSFromIndex = (
  g: DirectedGraph,
  start_index: number,
  f: vertexFunction
) => {
  const edgesBySrc = edgesBySrcToMap(g.Edges);

  const visit = (vertexIndex: number) => {
    if (f(g.Vertices[vertexIndex], vertexIndex) === false) {
      return;
    }
    const next = edgesBySrc.get(vertexIndex);
    if (next === undefined) {
      return;
    }
    next.forEach((e: DirectedEdge) => {
      visit(e.j);
    });
  };

  visit(start_index);
};

/**
The return type for the ToplogicalSort function. 
 */
type TSReturn = {
  hasCycles: boolean;

  cycle: VertexIndices;

  order: VertexIndices;
};

/**
Returns a topological sort order for a DirectedGraph, or the members of a cycle if a
topological sort can't be done.
 
 The topological sort comes from:

    https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search

L ← Empty list that will contain the sorted nodes
while exists nodes without a permanent mark do
    select an unmarked node n
    visit(n)

function visit(node n)
    if n has a permanent mark then
        return
    if n has a temporary mark then
        stop   (graph has at least one cycle)

    mark n with a temporary mark

    for each node m with an edge from n to m do
        visit(m)

    remove temporary mark from n
    mark n with a permanent mark
    add n to head of L

 */
const TopologicalSort = (g: DirectedGraph): TSReturn => {
  const ret: TSReturn = {
    hasCycles: false,
    cycle: [],
    order: [],
  };

  const edgeMap = edgesBySrcToMap(g.Edges);

  const nodesWithoutPermanentMark = new Set<number>();
  g.Vertices.forEach((_: Vertex, index: number) =>
    nodesWithoutPermanentMark.add(index)
  );

  const hasPermanentMark = (index: number): boolean => {
    return !nodesWithoutPermanentMark.has(index);
  };

  const temporaryMark = new Set<number>();

  const visit = (index: number): boolean => {
    if (hasPermanentMark(index)) {
      return true;
    }
    if (temporaryMark.has(index)) {
      // We only return false on finding a loop, which is stored in
      // temporaryMark.
      return false;
    }
    temporaryMark.add(index);

    const nextEdges = edgeMap.get(index);
    if (nextEdges !== undefined) {
      for (let i = 0; i < nextEdges.length; i++) {
        const e = nextEdges[i];
        if (!visit(e.j)) {
          return false;
        }
      }
    }

    temporaryMark.delete(index);
    nodesWithoutPermanentMark.delete(index);
    ret.order.unshift(index);
    return true;
  };

  // We will presume that Vertex[0] is the start node and that we should start there.
  const ok = visit(0);
  if (!ok) {
    ret.hasCycles = true;
    ret.cycle = [...temporaryMark.keys()];
  }

  return ret;
};

/** Task is a Vertex with details about the Task to complete. */
class Task {
  constructor(
    name: string = "",
    duration: number = 0,
    optimisticDuration: number = 0,
    pessimisticDuration: number = 0
  ) {
    if (name === "") {
      this.name = "Task Name";
    } else {
      this.name = name;
    }
    this.duration = duration;
    if (optimisticDuration) {
      this.optimisticDuration = optimisticDuration;
    } else {
      this.optimisticDuration = duration;
    }
    if (pessimisticDuration) {
      this.pessimisticDuration = pessimisticDuration;
    } else {
      this.pessimisticDuration = duration;
    }
  }

  name: string;

  // How long does this task take. Note this value is unitless, so it could be
  // seconds, days, or years.
  duration: number;

  // TODO: How do we handle different variability mechanisms, e.g. using a Beta function instead?

  // The optimistic and pessimistic estimates of how long this task will take to
  // complete.
  optimisticDuration: number;
  pessimisticDuration: number;
}

/** The standard PERT slack calculation values. */
class Slack {
  earlyStart: number = 0;
  earlyFinish: number = 0;
  lateStart: number = 0;
  lateFinish: number = 0;
  slack: number = 0;
}

type Tasks = Task[];

/** A Chart is a DirectedGraph, but with Tasks for Vertices. */
class Chart {
  Vertices: Tasks = [new Task(), new Task()];
  Edges: Edges = [];
}

type TopologicalOrder = VertexIndices;

/** Result allows easier handling of returning either an error or a value from a
 * function. */
export type Result<T> = { ok: true; value: T } | { ok: false; error: Error };

function ok<T>(value: T): Result<T> {
  return { ok: true, value: value };
}

function error<T>(value: string | Error): Result<T> {
  if (typeof value === "string") {
    return { ok: false, error: new Error(value) };
  }
  return { ok: false, error: value };
}

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
  const tsRet = TopologicalSort(g);
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

const C: Chart = {
  Vertices: [
    new Task("Start"),
    new Task("A", 10),
    new Task("B", 15, 7, 20),
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
  "Tasks on the critical path for optimistic time:",
  ComputeSlack(C, (t: Task) => t.optimisticDuration)
);

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
// These records the sub-ops for each large op. E.g. an insert task op is made
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
  apply(c: Chart): Result<Chart>;
  inverse(): SubOp;
}

class Op {
  constructor(subOps: SubOp[]) {
    this.subOps = subOps;
  }

  subOps: SubOp[] = [];

  inverse(): Op {
    return new Op(this.subOps.reverse().map((s: SubOp) => s.inverse()));
  }
}

class AddEdgeSubOp implements SubOp {
  i: number = 0;
  j: number = 0;

  constructor(i: number, j: number) {
    this.i = i;
    this.j = j;
  }

  apply(c: Chart): Result<Chart> {
    if (this.i < 0 || this.i >= c.Vertices.length) {
      return error(
        `i index out of range: ${this.i} not in [0, ${c.Vertices.length - 1}]`
      );
    }
    if (this.j < 0 || this.j >= c.Vertices.length) {
      return error(
        `j index out of range: ${this.j} not in [0, ${c.Vertices.length - 1}]`
      );
    }
    if (this.i === this.j) {
      return error(`A Task can not depend on itself: ${this.i} === ${this.j}`);
    }
    c.Edges.push(new DirectedEdge(this.i, this.j));
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
    if (this.i < 0 || this.i >= c.Vertices.length) {
      return error(
        `i index out of range: ${this.i} not in [0, ${c.Vertices.length - 1}]`
      );
    }
    if (this.j < 0 || this.j >= c.Vertices.length) {
      return error(
        `j index out of range: ${this.j} not in [0, ${c.Vertices.length - 1}]`
      );
    }
    if (this.i === this.j) {
      return error(`A Task can not depend on itself: ${this.i} === ${this.j}`);
    }
    c.Edges = c.Edges.filter((v: DirectedEdge): boolean => {
      if (v.i === this.i && v.j === this.j) {
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

function insertNewEmptyTaskAfter(c: Chart, index: number): Result<Chart> {
  // Check that index makes sense, can't be less than 0, and can't be the Finish Task either.

  const ret: Chart = new Chart();

  // First copy over the Tasks.

  // Then insert new Task.

  // Add new Update all Edges that have an 'i' or 'j' that is >= index.

  // Add Start and Finish edges for the new Task.

  // Validate Chart

  // Add a revert operations group to the Undo Stack.

  return ok(ret);
}
