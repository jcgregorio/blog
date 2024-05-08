import {
  Vertex,
  VertexIndices,
  DirectedEdge,
  Edges,
  DirectedGraph,
  edgesBySrcToMap,
  edgesByDstToMap,
} from "../dag.ts";

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
export const topologicalSort = (g: DirectedGraph): TSReturn => {
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
