import { Chart, Task } from "../chart/chart.ts";
import { Result, ok, error } from "../result.ts";
import { DirectedEdge } from "../dag/dag.ts";

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

export interface SubOp {
  // If the apply returns an error it is guaranteed not to have modified the
  // Chart.
  apply(c: Chart): Result<Chart>;

  inverse(): SubOp;
}

export class Op {
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
export function DirectedEdgeForChart(
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

export class AddEdgeSubOp implements SubOp {
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

export class RemoveEdgeSupOp implements SubOp {
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

export class AddTaskAfterSubOp implements SubOp {
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

export class DeleteTaskAfterSubOp implements SubOp {
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

export function InsertNewEmptyTaskAfterOp(index: number): Op {
  return new Op([
    new AddTaskAfterSubOp(index),
    new AddEdgeSubOp(0, index + 1),
    new AddEdgeSubOp(index + 1, -1),
  ]);
}
