---
title: "Project Management"
date: 2024-04-21T12:58:12-04:00
---

Let's talk about project planning. We'll start off with a large and complex
task, like building a house.

![A simple plan for building a house with a sinlge task labelled "Build House".](./plan1.excalidraw.png)

Note that we can decide when to _start_ building the house, but when we _finish_
the house is unknown. This is the entire point of project management, given a
start time and a task, figuring out when it will end. All of our efforts will
revolve around trying to reduce that ambiquity.

Sure, we will also track cost, resouce allocation, and other attributes of a
task as the project goes on, but that is almost always **in service of a finish
time**.

The fundamental nature of the ambiguity of the finish time of a task is
something I regularly see get lost in project management, and think that might
be caused, in part, by the tools we use to track project progress, in particular
the visial representation of that information. Look at the above image and see
the very definite end of the task. I think drawing the task in a slightly
different way would stress the ambiguity around the finish, for example:

![A simple plan for building a house with a sinlge task labelled "Build House",
but the right hand side of the task is drawn in a ragged
manner.](./uncertain.excalidraw.png)

Reducing uncertainty about the duration of a task is the fundamental mission of
project management.

So how do we go about reducing that ambiguity? The first step is to break down
that that one monolithic task into a series of smaller intermediate steps. The
idea being that the smaller tasks will also have less ambiguity associated with
them. So let's start breaking down our house building task into smaller
sub-tasks:

- Design
- Permit
- Site Prep
- Pour Foundation
- Foundation inspection
- Rough framing
- Roof
- Electrical rough-in
- Plumbing rough-in
- HVAC
- Windows and Doors
- House wrap
- Siding
- Insulation
- Drywall
- Interior Paint
- Exterior Paint
- Finish Electrical
- Flooring
- Cabinetry
- Counter tops

This list obviouisly not comprehensive, but you get the idea.

What we also know is that there are estimated durations for each of these tasks,
and they have some ordering on them. For example, we can't do Eletrical rough-in
until after the rough framing and roof are complete. That is, Electrical
Rough-In is dependent on the Roof being completed. There are dependencies all
among these tasks. Let's look at a small section of what that tree of
dependencies looks like:

![A tree diagram showing that both Electrical Rough-In and Plumbing Rough-In
can't start until the Roof is complete.](./deps.excalidraw.png)

This [Work Breakdown
Structure](https://en.wikipedia.org/wiki/Work_breakdown_structure) is an
important piece of project planning, requiring you to think about the sub-tasks
and ask questions about their dependencies. Those dependencies build out
a tree structure.
