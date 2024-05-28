import { Result, ok, error } from "../result.ts";
import { Task, Chart, ChartValidate } from "../chart/chart.ts";
import { DirectedEdge, edgesByDstToMap, edgesBySrcToMap } from "../dag/dag.ts";

/** The standard slack calculation values. */
export class Slack {
  earlyStart: number = 0;
  earlyFinish: number = 0;
  lateStart: number = 0;
  lateFinish: number = 0;
  slack: number = 0;
}

export type TaskDuration = (t: Task) => number;

export const defaultTaskDuration = (t: Task): number => {
  return t.duration;
};

export type SlackResult = Result<Slack[]>;

// Calculate the slack for each Task in the Chart.
export function ComputeSlack(
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
