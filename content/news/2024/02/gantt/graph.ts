type Vertex = {
  weight: number;
};

type Edge = {
  i: number;
  j: number;
};

type Vertices = Vertex[];

// Would this be better as a Set<Edge> ?
type Edges = Edge[];

type Graph = {
  Vertices: Vertices;
  Edges: Edges;
};

const edgesBySrcToMap = (edges: Edges): Map<number, Edges> => {
  const ret = new Map<number, Edges>();

  edges.forEach((e: Edge) => {
    const arr = ret.get(e.i) || [];
    arr.push(e);
    ret.set(e.i, arr);
  });

  return ret;
};

const edgesByDstToMap = (edges: Edges): Map<number, Edges> => {
  const ret = new Map<number, Edges>();

  edges.forEach((e: Edge) => {
    const arr = ret.get(e.j) || [];
    arr.push(e);
    ret.set(e.j, arr);
  });

  return ret;
};

type vertexFunction = (v: Vertex, index: number) => boolean;

const SetOfVerticesWithNoIncomingEdge = (g: Graph): number[] => {
  const nodesWithIncomingEdges = edgesByDstToMap(g.Edges);
  const ret: number[] = [];
  G.Vertices.forEach((_: Vertex, i: number) => {
    if (!nodesWithIncomingEdges.has(i)) {
      ret.push(i);
    }
  });
  return ret;
};

const DFS = (g: Graph, f: vertexFunction) => {
  SetOfVerticesWithNoIncomingEdge(g).forEach((vertexIndex: number) => {
    DFSFromIndex(g, vertexIndex, f);
  });
};

/** Depth First Search starting at start_vertex. */
const DFSFromIndex = (g: Graph, startVertex: number, f: vertexFunction) => {
  const edgesBySrc = edgesBySrcToMap(g.Edges);

  const visit = (vertexIndex: number) => {
    if (f(g.Vertices[vertexIndex], vertexIndex) === false) {
      return;
    }
    const next = edgesBySrc.get(vertexIndex);
    if (next === undefined) {
      return;
    }
    next.forEach((e: Edge) => {
      visit(e.j);
    });
  };

  visit(startVertex);
};

// Confirming that a PERTNode can be used as a Vertex.
type PERTNode = {
  optimisticWeight: 10;
  pessimisticWeight: 20;
} & Vertex;

var pertNode: PERTNode = {
  weight: 12,
  optimisticWeight: 10,
  pessimisticWeight: 20,
};

const G: Graph = {
  Vertices: [{ weight: 0 }, { weight: 10 }, { weight: 20 }, pertNode],
  Edges: [
    { i: 0, j: 1 },
    { i: 0, j: 2 },
    { i: 1, j: 3 },
    { i: 2, j: 3 },
  ],
};

function IsChart(g: Graph): string {
  var ret = true;
  const edgesByDst = edgesByDstToMap(g.Edges);
  // The first Vertex, the Start node, must have 0 incoming edges.
  if (edgesByDst.get(0) !== undefined) {
    return "The start node (0) has an incoming edge.";
  }

  console.log("edgesByDst", edgesByDst);
  // And only T_0 should have 0 incoming edges.
  for (let i = 1; i < G.Vertices.length; i++) {
    if (edgesByDst.get(i) === undefined) {
      return `Found node that isn't (0) that has no incoming edges: ${i}`;
    }
  }

  // Now we confirm that the graph has no cycles by creating a topological sort starting at T_0
  // https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search
  const tsRet = TopologicalSort(g);
  if (tsRet.hasCycles) {
    return "Chart has cycles";
  }
  return "";
}

type TSReturn = {
  hasCycles: boolean;
  order: number[];
};

/*

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

const TopologicalSort = (g: Graph): TSReturn => {
  const ret: TSReturn = {
    hasCycles: false,
    order: [],
  };

  const edgeMap = edgesBySrcToMap(g.Edges);

  const nodesWithoutPermanentMark = new Set<number>();
  G.Vertices.forEach((_: Vertex, index: number) =>
    nodesWithoutPermanentMark.add(index)
  );

  const hasPermanentMark = (index: number): boolean => {
    return !nodesWithoutPermanentMark.has(index);
  };

  const temporaryMark = new Set<number>();

  const visit = (index: number): void => {
    if (hasPermanentMark(index)) {
      return;
    }
    if (temporaryMark.has(index)) {
      throw `Found a cycle among the following nodes ${[
        ...temporaryMark.keys(),
      ].join(", ")}`;
    }
    temporaryMark.add(index);
    console.log("temporaryMark", temporaryMark);

    const nextEdges = edgeMap.get(index);
    if (nextEdges !== undefined) {
      nextEdges.forEach((e: Edge) => {
        visit(e.j);
      });
    }

    temporaryMark.delete(index);
    nodesWithoutPermanentMark.delete(index);
    ret.order.unshift(index);
  };

  // We will presume that Vertex[0] is the start node and that we should start there.
  visit(0);

  return ret;
};

console.log("IsChart:", TopologicalSort(G).order);
