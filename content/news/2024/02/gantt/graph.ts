type Vertex = {
  weight: number;
};

type Edge = {
  i: number;
  j: number;
};

type Vertices = Vertex[];

type Edges = Edge[];

type Graph = {
  Vertices: Vertices;
  Edges: Edges;
};

function edgesToMap(edges: Edges): { [index: number]: Edge[] } {
  const ret: { [index: number]: Edge[] } = {};

  edges.forEach((e: Edge) => {
    const arr = ret[e.i] || [];
    arr.push(e);
    ret[e.i] = arr;
  });

  return ret;
}

function IsDAG(g: Graph): boolean {
  const seen: Vertex[] = [];
  const edgeMap = edgesToMap(g.Edges);
  g.Vertices.forEach((v: Vertex) => {});
  return true;
}
