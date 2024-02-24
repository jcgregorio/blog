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

function edgesSrcToMap(edges: Edges): Map<number, Edges> {
  const ret = new Map<number, Edges>();

  edges.forEach((e: Edge) => {
    const arr = ret.get(e.i) || [];
    arr.push(e);
    ret.set(e.i, arr);
  });

  return ret;
}

function edgesDstToMap(edges: Edges): Map<number, Edges> {
  const ret = new Map<number, Edges>();

  edges.forEach((e: Edge) => {
    const arr = ret.get(e.j) || [];
    arr.push(e);
    ret.set(e.j, arr);
  });

  return ret;
}

type vertexFunction = (v: Vertex, index: number) => boolean;

function DFS(g: Graph, start_vertex: number, f: vertexFunction) {
  const edgesBySrc = edgesSrcToMap(g.Edges);

  const visit = (index: number) => {
    f(g.Vertices[index], index);
    const next = edgesBySrc.get(index);
    if (next === undefined) {
      return;
    }
    next.forEach((e: Edge) => {
      visit(e.j);
    });
  };

  visit(start_vertex);
}

const G: Graph = {
  Vertices: [{ weight: 0 }, { weight: 10 }, { weight: 20 }, { weight: 15 }],
  Edges: [
    { i: 0, j: 1 },
    { i: 0, j: 2 },
    { i: 1, j: 3 },
    { i: 2, j: 3 },
  ],
};

DFS(G, 0, (v: Vertex, index: number) => {
  console.log(v.weight, index);
  return true;
});

/*
function IsDAG(g: Graph): boolean {
  const seen: Vertex[] = [];
  const edgeMap = edgesSrcToMap(g.Edges);
  g.Vertices.forEach((v: Vertex, i: number) => {
    const edges = edgeMap.get(i);
    if (edges === undefined) {
      return;
    }
  });
  return true;
}
*/
