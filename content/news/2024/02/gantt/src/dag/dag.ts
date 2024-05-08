/** One vertex of a graph. */
export type Vertex = {};

/** Every Vertex in a graph. */
export type Vertices = Vertex[];

/** A subset of Vertices referred to by their index number. */
export type VertexIndices = number[];

/** One edge of a graph, which is a directed connection from the i'th Vertex to
the j'th Vertex, where the Vertex is stored in a Vertices.
 */
export class DirectedEdge {
  i: number = 0;
  j: number = 0;

  constructor(i: number, j: number) {
    this.i = i;
    this.j = j;
  }
}

/** Every Egde in a graph. */
export type Edges = DirectedEdge[];

/** A graph is just a collection of Vertices and Edges between those vertices. */
export type DirectedGraph = {
  Vertices: Vertices;
  Edges: Edges;
};

/**
 Groups the Edges by their `i` value.

 @param edges - All the Eges in a DirectedGraph.
 @returns A map from the Vertex index to all the Edges that start at
   at that Vertex index.
 */
export const edgesBySrcToMap = (edges: Edges): Map<number, Edges> => {
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

export const edgesByDstToMap = (edges: Edges): Map<number, Edges> => {
  const ret = new Map<number, Edges>();

  edges.forEach((e: DirectedEdge) => {
    const arr = ret.get(e.j) || [];
    arr.push(e);
    ret.set(e.j, arr);
  });

  return ret;
};
