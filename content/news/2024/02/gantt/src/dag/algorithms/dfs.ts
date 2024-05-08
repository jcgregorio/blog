import { Result, ok, error } from "../../result.ts";
import {
  Vertex,
  VertexIndices,
  DirectedEdge,
  Edges,
  DirectedGraph,
  edgesBySrcToMap,
  edgesByDstToMap,
} from "../dag.ts";

/** A function that can be applied to a Vertex, used in later functions like
Depth First Search to do work on every Vertex in a DirectedGraph.
 */
export type vertexFunction = (v: Vertex, index: number) => boolean;

/** Returns the index of all Vertices that have no incoming edge.
 */
export const setOfVerticesWithNoIncomingEdge = (
  g: DirectedGraph
): VertexIndices => {
  const nodesWithIncomingEdges = edgesByDstToMap(g.Edges);
  const ret: VertexIndices = [];
  g.Vertices.forEach((_: Vertex, i: number) => {
    if (!nodesWithIncomingEdges.has(i)) {
      ret.push(i);
    }
  });
  return ret;
};

/** Descends the graph in Depth First Search and applies the function `f` to
each node.
 */
export const depthFirstSearch = (g: DirectedGraph, f: vertexFunction) => {
  setOfVerticesWithNoIncomingEdge(g).forEach((value: Vertex, index: number) => {
    depthFirstSearchFromIndex(g, index, f);
  });
};

/** Depth First Search starting at Vertex `start_index`. */
export const depthFirstSearchFromIndex = (
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
