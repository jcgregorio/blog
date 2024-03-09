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
  constructor(duration: number = 0) {
    this.duration = duration;
  }

  // How long does this task take. Note this value is unitless, so it could be
  // seconds, days, or years.
  duration: number;

  // TODO: How do we handle different variability mechanisms, i.e. using a Beta function instead?

  // The optimistic and pessimistic estimates of how long this task will take to
  // complete.
  optimisticDuration: number = 0;
  pessimisticDuration: number = 0;

  // The calculated slack values for this Task.
  earlyStart: number = 0;
  earlyFinish: number = 0;
  lateStart: number = 0;
  lateFinish: number = 0;
  slack: number = 0;
}

type Tasks = Task[];

/** A Chart is a DirectedGraph, but with Tasks for Vertices. */
class Chart {
  Vertices: Tasks = [new Task()];
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
  if (g.Vertices.length === 0) {
    return error("Chart must contain at least one node.");
  }

  const edgesByDst = edgesByDstToMap(g.Edges);
  // The first Vertex, the Start node, must have 0 incoming edges.
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

// Do some testing.

const G: DirectedGraph = {
  Vertices: [{}, {}, {}],
  Edges: [
    { i: 0, j: 1 },
    { i: 0, j: 2 },
    { i: 1, j: 3 },
    { i: 2, j: 3 },
  ],
};

const GWithLoop: DirectedGraph = {
  Vertices: [{}, {}, {}],
  Edges: [
    { i: 0, j: 1 },
    { i: 0, j: 2 },
    { i: 1, j: 3 },
    { i: 2, j: 3 },
    { i: 3, j: 1 },
  ],
};

/*
console.log("IsChart:", Validate(new Chart()));
console.log("IsChart:", Validate(G));
console.log("IsChart:", Validate(GWithLoop));
*/

const C: Chart = {
  Vertices: [new Task(), new Task(10), new Task(15), new Task(8)],
  Edges: [
    { i: 0, j: 1 },
    { i: 0, j: 2 },
    { i: 1, j: 3 },
    { i: 2, j: 3 },
  ],
};

type SlackResult = Result<VertexIndices>;

function Slack(c: Chart): SlackResult {
  const ret: VertexIndices = [];
  const r = Validate(c);
  if (!r.ok) {
    return error(r.error);
  }

  const edgesByDst = edgesByDstToMap(C.Edges);
  const edgesBySrc = edgesBySrcToMap(C.Edges);

  const topologicalOrder = r.value;

  topologicalOrder.slice(1).forEach((vertexIndex: number) => {
    const task = C.Vertices[vertexIndex];
    task.earlyStart = Math.max(
      ...edgesByDst.get(vertexIndex)!.map((e: DirectedEdge): number => {
        const predecessorTask = C.Vertices[e.i];
        return predecessorTask.earlyFinish;
      })
    );
    task.earlyFinish = task.earlyStart + task.duration;
  });

  topologicalOrder.reverse().forEach((vertexIndex: number) => {
    const task = C.Vertices[vertexIndex];
    const successors = edgesBySrc.get(vertexIndex);
    if (!successors) {
      task.lateFinish = task.earlyFinish;
      task.lateStart = task.earlyStart;
      if (task.slack === 0) {
        ret.push(vertexIndex);
      }

      return;
    }
    task.lateFinish = Math.min(
      ...edgesBySrc.get(vertexIndex)!.map((e: DirectedEdge): number => {
        const successorTask = C.Vertices[e.j];
        return successorTask.lateStart;
      })
    );
    task.lateStart = task.lateFinish - task.duration;
    // Determine slack.
    task.slack = task.lateFinish - task.earlyFinish;

    if (task.slack === 0) {
      ret.push(vertexIndex);
    }
  });

  return ok(ret);
}

console.log(Slack(C));
